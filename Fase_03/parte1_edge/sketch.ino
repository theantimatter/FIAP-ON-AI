/*
  CardioIA - Fase 3 - Parte 1: Edge Computing
  Diego Filipe Pereira de Araujo - RM567064

  Wearable cardíaco simulado no ESP32.
  Sensores:
    - DHT22 (temperatura e umidade)        -> GPIO 15
    - Botão de pulso (cada toque = 1 batida) -> GPIO 4
  Atuadores / controles:
    - Chave deslizante que simula o Wi-Fi  -> GPIO 18 (direita = conectado)
    - LED vermelho de alerta local         -> GPIO 13

  Lógica de resiliência (store and forward):
    Toda leitura entra primeiro num buffer circular em RAM. A leitura só sai do
    buffer depois de "enviada para a nuvem" (Serial.println com prefixo [NUVEM]).
    Sem conexão, o buffer vai acumulando; quando a conexão volta, as leituras
    pendentes são enviadas da mais antiga para a mais nova e apagadas.
    No simulador o SPIFFS é volátil, então o buffer fica em RAM e o Monitor
    Serial faz o papel do registro offline.
*/

#include "DHTesp.h"

// ---------- Pinos ----------
const int PINO_DHT    = 15;
const int PINO_PULSO  = 4;
const int PINO_WIFI   = 18;
const int PINO_ALERTA = 13;

// ---------- Tempos ----------
const unsigned long INTERVALO_LEITURA_MS = 5000;  // uma amostra a cada 5 s
const unsigned long PULSO_TIMEOUT_MS     = 4000;  // sem toque por 4 s = sem pulso

// ---------- Buffer offline ----------
// 2880 amostras x 5 s = 4 horas sem conexão (ver relatório)
const int CAPACIDADE_BUFFER = 2880;
const int LOTE_ENVIO        = 20;   // quantas leituras enviar por volta do loop

// ---------- Limites de alerta ----------
const float TEMP_FEBRE      = 38.0;
const float TEMP_HIPOTERMIA = 35.0;
const int   BPM_TAQUICARDIA = 120;
const int   BPM_BRADICARDIA = 50;

struct Leitura {
  uint32_t id;        // número sequencial da amostra
  uint32_t segundos;  // tempo desde que o dispositivo ligou
  float temperatura;
  float umidade;
  uint16_t bpm;
};

Leitura buffer[CAPACIDADE_BUFFER];
int inicio = 0;      // posição da leitura mais antiga
int quantidade = 0;  // leituras guardadas esperando envio
uint32_t proximoId = 1;
uint32_t descartadas = 0;
int totalSincronizadas = 0;  // soma dos lotes até o buffer esvaziar

DHTesp dht;

bool wifiConectado = false;
unsigned long ultimaLeitura = 0;

// Variáveis do batimento
const int N_INTERVALOS = 4;
unsigned long intervalos[N_INTERVALOS];
int nIntervalos = 0;
int posIntervalo = 0;
unsigned long ultimoPulso = 0;
int estadoBotaoAnterior = HIGH;
unsigned long ultimaMudancaBotao = 0;

// ---------------------------------------------------------------------------
// Buffer circular
// ---------------------------------------------------------------------------

void guardarLeitura(const Leitura &l) {
  if (quantidade == CAPACIDADE_BUFFER) {
    // Buffer cheio: sobrescreve a mais antiga. Para monitoramento cardíaco
    // a informação recente vale mais que a de horas atrás.
    inicio = (inicio + 1) % CAPACIDADE_BUFFER;
    quantidade--;
    descartadas++;
  }
  int fim = (inicio + quantidade) % CAPACIDADE_BUFFER;
  buffer[fim] = l;
  quantidade++;
}

void removerMaisAntiga() {
  inicio = (inicio + 1) % CAPACIDADE_BUFFER;
  quantidade--;
}

// ---------------------------------------------------------------------------
// Sensor de pulso (botão)
// ---------------------------------------------------------------------------

void lerBotaoPulso() {
  int estado = digitalRead(PINO_PULSO);
  unsigned long agora = millis();

  // debounce simples de 30 ms
  if (estado != estadoBotaoAnterior && agora - ultimaMudancaBotao > 30) {
    ultimaMudancaBotao = agora;
    estadoBotaoAnterior = estado;

    if (estado == LOW) {  // botão apertado = uma batida
      unsigned long intervalo = agora - ultimoPulso;
      // aceita só intervalos entre 30 e 240 bpm, o resto é ruído
      if (ultimoPulso > 0 && intervalo >= 250 && intervalo <= 2000) {
        intervalos[posIntervalo] = intervalo;
        posIntervalo = (posIntervalo + 1) % N_INTERVALOS;
        if (nIntervalos < N_INTERVALOS) nIntervalos++;
      }
      ultimoPulso = agora;
    }
  }
}

int calcularBpm() {
  if (ultimoPulso == 0 || millis() - ultimoPulso > PULSO_TIMEOUT_MS) {
    nIntervalos = 0;
    return 0;
  }
  if (nIntervalos == 0) return 0;

  unsigned long soma = 0;
  for (int i = 0; i < nIntervalos; i++) soma += intervalos[i];
  return 60000 / (soma / nIntervalos);
}

// ---------------------------------------------------------------------------
// Alerta local
// ---------------------------------------------------------------------------

bool verificarAlerta(const Leitura &l) {
  bool febre = l.temperatura >= TEMP_FEBRE;
  bool hipotermia = l.temperatura < TEMP_HIPOTERMIA;
  bool taquicardia = l.bpm > BPM_TAQUICARDIA;
  bool bradicardia = l.bpm > 0 && l.bpm < BPM_BRADICARDIA;

  if (febre) Serial.println("  ALERTA: febre");
  if (hipotermia) Serial.println("  ALERTA: temperatura baixa");
  if (taquicardia) Serial.println("  ALERTA: taquicardia");
  if (bradicardia) Serial.println("  ALERTA: bradicardia");

  return febre || hipotermia || taquicardia || bradicardia;
}

// ---------------------------------------------------------------------------
// Coleta e envio
// ---------------------------------------------------------------------------

void coletarAmostra() {
  TempAndHumidity dados = dht.getTempAndHumidity();
  if (dht.getStatus() != 0) {
    Serial.println("[ERRO] falha na leitura do DHT22, amostra ignorada");
    return;
  }

  Leitura l;
  l.id = proximoId++;
  l.segundos = millis() / 1000;
  l.temperatura = dados.temperature;
  l.umidade = dados.humidity;
  l.bpm = calcularBpm();

  guardarLeitura(l);

  Serial.printf("[LEITURA] #%lu  T=%.1f C  U=%.1f %%  BPM=%u  | buffer %d/%d\n",
                (unsigned long)l.id, l.temperatura, l.umidade, l.bpm,
                quantidade, CAPACIDADE_BUFFER);

  // o alerta local funciona mesmo sem internet
  digitalWrite(PINO_ALERTA, verificarAlerta(l) ? HIGH : LOW);
}

void enviarPendentes() {
  int enviadas = 0;
  while (quantidade > 0 && enviadas < LOTE_ENVIO) {
    Leitura &l = buffer[inicio];
    // simula o envio para a nuvem em formato JSON
    Serial.printf("[NUVEM] {\"id\":%lu,\"t\":%lu,\"temp\":%.1f,\"umid\":%.1f,\"bpm\":%u}\n",
                  (unsigned long)l.id, (unsigned long)l.segundos,
                  l.temperatura, l.umidade, l.bpm);
    removerMaisAntiga();  // apaga do armazenamento local depois de enviar
    enviadas++;
  }
  totalSincronizadas += enviadas;

  // só avisa quando descarregou leituras acumuladas, não a cada envio normal
  if (quantidade == 0) {
    if (totalSincronizadas > 1) {
      Serial.printf("[SYNC] %d leituras sincronizadas, buffer vazio\n", totalSincronizadas);
    }
    totalSincronizadas = 0;
  }
}

void atualizarWifi() {
  bool estado = digitalRead(PINO_WIFI) == HIGH;
  if (estado != wifiConectado) {
    wifiConectado = estado;
    if (wifiConectado) {
      Serial.printf("\n[WIFI] CONECTADO - %d leitura(s) pendente(s) para sincronizar\n", quantidade);
      if (descartadas > 0) {
        Serial.printf("[WIFI] %lu leitura(s) antiga(s) foram descartadas por falta de espaco\n",
                      (unsigned long)descartadas);
        descartadas = 0;
      }
    } else {
      Serial.println("\n[WIFI] DESCONECTADO - modo offline, leituras ficam no buffer");
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.setup(PINO_DHT, DHTesp::DHT22);

  pinMode(PINO_PULSO, INPUT_PULLUP);
  pinMode(PINO_WIFI, INPUT_PULLUP);
  pinMode(PINO_ALERTA, OUTPUT);

  Serial.println("CardioIA - wearable cardiaco (Edge)");
  Serial.printf("Buffer offline: %d amostras (%d min a cada %lu s)\n",
                CAPACIDADE_BUFFER,
                (int)(CAPACIDADE_BUFFER * (INTERVALO_LEITURA_MS / 1000) / 60),
                INTERVALO_LEITURA_MS / 1000);

  wifiConectado = !(digitalRead(PINO_WIFI) == HIGH);  // força mensagem inicial
  atualizarWifi();
}

void loop() {
  lerBotaoPulso();
  atualizarWifi();

  if (millis() - ultimaLeitura >= INTERVALO_LEITURA_MS) {
    ultimaLeitura = millis();
    coletarAmostra();
  }

  if (wifiConectado) {
    enviarPendentes();
  }
}
