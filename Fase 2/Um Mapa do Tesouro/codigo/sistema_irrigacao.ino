#include <DHT.h>

#define DHTPIN 15
#define DHTTYPE DHT22
#define LDR_PIN 34
#define BOTAO_N 12
#define BOTAO_P 14
#define BOTAO_K 27
#define RELE_BOMBA 26

DHT dht(DHTPIN, DHTTYPE);

bool nitrogenio = false;
bool fosforo = false;
bool potassio = false;
float umidade = 0;
float ph = 0;
bool bomba_ligada = false;

bool botao_n_anterior = HIGH;
bool botao_p_anterior = HIGH;
bool botao_k_anterior = HIGH;

void setup()
{
  Serial.begin(115200);

  pinMode(BOTAO_N, INPUT_PULLUP);
  pinMode(BOTAO_P, INPUT_PULLUP);
  pinMode(BOTAO_K, INPUT_PULLUP);
  pinMode(RELE_BOMBA, OUTPUT);

  dht.begin();

  digitalWrite(RELE_BOMBA, LOW);
}

void loop()
{
  bool botao_n_atual = digitalRead(BOTAO_N);
  if (botao_n_anterior == HIGH && botao_n_atual == LOW) {
    nitrogenio = !nitrogenio;
    Serial.print(">>> Nitrogenio alternado para: ");
    Serial.println(nitrogenio ? "OK" : "BAIXO");
    delay(50);
  }
  botao_n_anterior = botao_n_atual;

  bool botao_p_atual = digitalRead(BOTAO_P);
  if (botao_p_anterior == HIGH && botao_p_atual == LOW) {
    fosforo = !fosforo;
    Serial.print(">>> Fosforo alternado para: ");
    Serial.println(fosforo ? "OK" : "BAIXO");
    delay(50);
  }
  botao_p_anterior = botao_p_atual;

  bool botao_k_atual = digitalRead(BOTAO_K);
  if (botao_k_anterior == HIGH && botao_k_atual == LOW) {
    potassio = !potassio;
    Serial.print(">>> Potassio alternado para: ");
    Serial.println(potassio ? "OK" : "BAIXO");
    delay(50);
  }
  botao_k_anterior = botao_k_atual;

  umidade = dht.readHumidity();

  int ldr_valor = analogRead(LDR_PIN);
  ph = map(ldr_valor, 0, 4095, 0, 140) / 10.0;

  Serial.println("=== Sistema de Irrigacao ===");
  Serial.print("Nitrogenio (N): ");
  Serial.println(nitrogenio ? "OK" : "BAIXO");
  Serial.print("Fosforo (P): ");
  Serial.println(fosforo ? "OK" : "BAIXO");
  Serial.print("Potassio (K): ");
  Serial.println(potassio ? "OK" : "BAIXO");
  Serial.print("pH do solo: ");
  Serial.println(ph);
  Serial.print("Umidade do solo: ");

  if (isnan(umidade))
  {
    Serial.println("ERRO: Sensor DHT22 nao conectado");
    umidade = 0;
  }
  else
  {
    Serial.print(umidade);
    Serial.println("%");
  }

  if (!isnan(umidade) && umidade < 60)
  {
    if (ph >= 5.5 && ph <= 7.0)
    {
      if (nitrogenio && fosforo && potassio)
      {
        digitalWrite(RELE_BOMBA, HIGH);
        bomba_ligada = true;
        Serial.println(">>> BOMBA LIGADA <<<");
      }
      else
      {
        digitalWrite(RELE_BOMBA, LOW);
        bomba_ligada = false;
        Serial.println(">>> BOMBA DESLIGADA - Falta nutrientes <<<");
      }
    }
    else
    {
      digitalWrite(RELE_BOMBA, LOW);
      bomba_ligada = false;
      Serial.println(">>> BOMBA DESLIGADA - pH inadequado <<<");
    }
  }
  else
  {
    digitalWrite(RELE_BOMBA, LOW);
    bomba_ligada = false;
    Serial.println(">>> BOMBA DESLIGADA - Solo umido <<<");
  }

  Serial.println();
  delay(2000);
}
