/*
  CardioIA - Fase 3 - Parte 2: transmissão MQTT (Fog/Cloud)
  Diego Filipe Pereira de Araujo - RM567064

  Mesmo wearable da Parte 1, agora publicando de verdade num broker MQTT.
    - DHT22 (temperatura e umidade)          -> GPIO 15
    - Botão de pulso (cada toque = 1 batida) -> GPIO 4
    - Chave "sinal" (esquerda = simula queda) -> GPIO 18
    - LED vermelho de alerta local           -> GPIO 13

  Broker: HiveMQ (broker.hivemq.com:1883)
  Tópicos:
    cardioia/rm567064/paciente01/sinais  -> leituras em JSON
    cardioia/rm567064/paciente01/status  -> "online" / "offline" (retido + LWT)

  As leituras continuam passando pelo buffer circular da Parte 1: só saem dele
  depois que o publish deu certo. Se o Wi-Fi ou o broker cair, nada se perde.
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include "DHTesp.h"

// ---------- Rede ----------
const char *WIFI_SSID  = "Wokwi-GUEST";
const char *WIFI_SENHA = "";

const char *MQTT_BROKER = "broker.hivemq.com";
const int   MQTT_PORTA  = 1883;
const char *TOPICO_SINAIS = "cardioia/rm567064/paciente01/sinais";
const char *TOPICO_STATUS = "cardioia/rm567064/paciente01/status";

// ---------- Pinos ----------
const int PINO_DHT    = 15;
const int PINO_PULSO  = 4;
const int PINO_SINAL  = 18;
const int PINO_ALERTA = 13;

// ---------- Tempos ----------
const unsigned long INTERVALO_LEITURA_MS = 5000;
const unsigned long PULSO_TIMEOUT_MS     = 4000;
const unsigned long RECONEXAO_MS         = 5000;

// ---------- Buffer offline ----------
const int CAPACIDADE_BUFFER = 2880;  // 4 horas de amostras a cada 5 s
const int LOTE_ENVIO        = 20;

// ---------- Limites de alerta ----------
const float TEMP_FEBRE      = 38.0;
const float TEMP_HIPOTERMIA = 35.0;
const int   BPM_TAQUICARDIA = 120;
const int   BPM_BRADICARDIA = 50;

struct Leitura {
  uint32_t id;
  uint32_t epoch;   // horário real via NTP (0 se ainda não sincronizou)
  float temperatura;
  float umidade;
  uint16_t bpm;
  bool coletadaOffline;  // true se foi lida enquanto estava sem conexão
};

Leitura buffer[CAPACIDADE_BUFFER];
int inicio = 0;
int quantidade = 0;
uint32_t proximoId = 1;
uint32_t descartadas = 0;
int totalSincronizadas = 0;  // soma dos lotes até o buffer esvaziar

DHTesp dht;
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

bool sinalLiberado = true;  // posição da chave
unsigned long ultimaLeitura = 0;
unsigned long ultimaTentativa = 0;

// Variáveis do batimento
const int N_INTERVALOS = 4;
unsigned long intervalos[N_INTERVALOS];
int nIntervalos = 0;
int posIntervalo = 0;
unsigned long ultimoPulso = 0;
int estadoBotaoAnterior = HIGH;
unsigned long ultimaMudancaBotao = 0;

// ---------------------------------------------------------------------------
// Buffer circular (igual à Parte 1)
// ---------------------------------------------------------------------------

void guardarLeitura(const Leitura &l) {
  if (quantidade == CAPACIDADE_BUFFER) {
    inicio = (inicio + 1) % CAPACIDADE_BUFFER;  // descarta a mais antiga
    quantidade--;
    descartadas++;
  }
  buffer[(inicio + quantidade) % CAPACIDADE_BUFFER] = l;
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

  if (estado != estadoBotaoAnterior && agora - ultimaMudancaBotao > 30) {
    ultimaMudancaBotao = agora;
    estadoBotaoAnterior = estado;

    if (estado == LOW) {
      unsigned long intervalo = agora - ultimoPulso;
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

bool emAlerta(const Leitura &l) {
  return l.temperatura >= TEMP_FEBRE || l.temperatura < TEMP_HIPOTERMIA ||
         l.bpm > BPM_TAQUICARDIA || (l.bpm > 0 && l.bpm < BPM_BRADICARDIA);
}

// ---------------------------------------------------------------------------
// Conexões (não bloqueantes, para a coleta nunca parar)
// ---------------------------------------------------------------------------

void conectarWifi() {
  Serial.print("[WIFI] conectando em ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_SENHA, 6);
}

bool conectarMqtt() {
  String clientId = "cardioia-esp32-" + String((uint32_t)ESP.getEfuseMac(), HEX);
  // LWT: se o ESP32 cair sem avisar, o broker publica "offline" sozinho
  bool ok = mqtt.connect(clientId.c_str(), TOPICO_STATUS, 1, true, "offline");
  if (ok) {
    mqtt.publish(TOPICO_STATUS, "online", true);
    Serial.printf("[MQTT] conectado ao broker - %d leitura(s) pendente(s)\n", quantidade);
  } else {
    Serial.printf("[MQTT] falha (rc=%d), nova tentativa em %lu s\n",
                  mqtt.state(), RECONEXAO_MS / 1000);
  }
  return ok;
}

void atualizarChaveSinal() {
  bool estado = digitalRead(PINO_SINAL) == HIGH;
  if (estado == sinalLiberado) return;
  sinalLiberado = estado;

  if (sinalLiberado) {
    Serial.println("\n[SINAL] chave ligada - reconectando");
    ultimaTentativa = 0;
  } else {
    Serial.println("\n[SINAL] chave desligada - simulando perda de conexao");
    if (mqtt.connected()) {
      mqtt.publish(TOPICO_STATUS, "offline", true);
      mqtt.disconnect();
    }
  }
}

bool online() {
  return sinalLiberado && WiFi.status() == WL_CONNECTED && mqtt.connected();
}

void manterConexao() {
  if (!sinalLiberado || mqtt.connected()) return;
  if (millis() - ultimaTentativa < RECONEXAO_MS && ultimaTentativa != 0) return;
  ultimaTentativa = millis();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[WIFI] sem conexao, aguardando...");
    return;
  }
  conectarMqtt();
}

// ---------------------------------------------------------------------------
// Coleta e publicação
// ---------------------------------------------------------------------------

void coletarAmostra() {
  TempAndHumidity dados = dht.getTempAndHumidity();
  if (dht.getStatus() != 0) {
    Serial.println("[ERRO] falha na leitura do DHT22, amostra ignorada");
    return;
  }

  Leitura l;
  l.id = proximoId++;
  time_t agora = time(nullptr);
  l.epoch = agora > 1700000000 ? (uint32_t)agora : 0;
  l.temperatura = dados.temperature;
  l.umidade = dados.humidity;
  l.bpm = calcularBpm();
  l.coletadaOffline = !online();

  guardarLeitura(l);

  bool alerta = emAlerta(l);
  digitalWrite(PINO_ALERTA, alerta ? HIGH : LOW);

  Serial.printf("[LEITURA] #%lu  T=%.1f C  U=%.1f %%  BPM=%u%s  | buffer %d/%d\n",
                (unsigned long)l.id, l.temperatura, l.umidade, l.bpm,
                alerta ? "  ALERTA" : "", quantidade, CAPACIDADE_BUFFER);
}

void publicarPendentes() {
  int enviadas = 0;
  while (quantidade > 0 && enviadas < LOTE_ENVIO) {
    Leitura &l = buffer[inicio];
    const char *origem = l.coletadaOffline ? "buffer" : "tempo_real";

    char payload[160];
    snprintf(payload, sizeof(payload),
             "{\"id\":%lu,\"ts\":%lu,\"temp\":%.1f,\"umid\":%.1f,\"bpm\":%u,\"origem\":\"%s\"}",
             (unsigned long)l.id, (unsigned long)l.epoch,
             l.temperatura, l.umidade, l.bpm, origem);

    if (!mqtt.publish(TOPICO_SINAIS, payload)) {
      Serial.println("[MQTT] publish falhou, leitura continua no buffer");
      break;  // só apaga o que foi entregue
    }
    Serial.printf("[MQTT] -> %s\n", payload);
    removerMaisAntiga();
    enviadas++;
  }
  totalSincronizadas += enviadas;

  if (quantidade == 0) {
    if (totalSincronizadas > 1) {
      Serial.printf("[SYNC] buffer sincronizado (%d leituras)\n", totalSincronizadas);
    }
    if (descartadas > 0) {
      Serial.printf("[SYNC] %lu leitura(s) antiga(s) descartadas por falta de espaco\n",
                    (unsigned long)descartadas);
      descartadas = 0;
    }
    totalSincronizadas = 0;
  }
}

void setup() {
  Serial.begin(115200);
  dht.setup(PINO_DHT, DHTesp::DHT22);

  pinMode(PINO_PULSO, INPUT_PULLUP);
  pinMode(PINO_SINAL, INPUT_PULLUP);
  pinMode(PINO_ALERTA, OUTPUT);

  Serial.println("CardioIA - wearable cardiaco (MQTT)");

  sinalLiberado = digitalRead(PINO_SINAL) == HIGH;
  conectarWifi();
  configTime(-3 * 3600, 0, "pool.ntp.org");  // horário de Brasília

  mqtt.setServer(MQTT_BROKER, MQTT_PORTA);
  mqtt.setKeepAlive(15);
}

void loop() {
  lerBotaoPulso();
  atualizarChaveSinal();
  manterConexao();
  mqtt.loop();

  if (millis() - ultimaLeitura >= INTERVALO_LEITURA_MS) {
    ultimaLeitura = millis();
    coletarAmostra();
  }

  if (online()) {
    publicarPendentes();
  }
}
