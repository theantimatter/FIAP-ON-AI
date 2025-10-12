# Sistema de Irrigação Inteligente - FarmTech Solutions

## Descrição do Projeto

Sistema automatizado de irrigação para cultivo de café que monitora:

- Níveis de nutrientes (NPK)
- pH do solo
- Umidade do solo
- Condições climáticas

## Cultura Escolhida: Café

O café necessita:

- **pH ideal:** entre 5.5 e 7.0
- **Umidade mínima:** 60%
- **Nutrientes:** Nitrogênio (N), Fósforo (P) e Potássio (K)

## Componentes Utilizados

### Hardware (Wokwi)

- 1x ESP32
- 1x DHT22 (sensor de umidade)
- 1x LDR (sensor de pH)
- 3x Botões (N, P, K)
- 1x Relé (bomba d'água)

### Conexões

- DHT22 → GPIO 15
- LDR → GPIO 34
- Botão N → GPIO 12
- Botão P → GPIO 14
- Botão K → GPIO 27
- Relé → GPIO 26

## Lógica de Funcionamento

A bomba d'água **LIGA** quando:

1. Umidade < 60%
2. pH entre 5.5 e 7.0
3. Todos os nutrientes (N, P, K) estão presentes

Caso contrário, a bomba permanece **DESLIGADA**.

## Arquivos do Projeto

- `sistema_irrigacao.ino` - Código principal do ESP32
- `diagram.json` - Diagrama do circuito Wokwi
- `consulta_clima.py` - Consulta API de clima (opcional)
- `analise_irrigacao.r` - Análise estatística em R (opcional)

## Como Usar

1. Acesse [Wokwi.com](https://wokwi.com)
2. Crie um novo projeto ESP32
3. Cole o código do arquivo `sistema_irrigacao.ino`
4. Monte o circuito conforme as conexões abaixo (ou importe o `diagram.json`)
5. Execute a simulação

## Opcional: Integração com API

O arquivo `consulta_clima.py` consulta a API Open-Meteo para verificar previsão de chuva.

Para usar:

1. Execute: `python consulta_clima.py`

## Opcional: Análise em R

O arquivo `analise_irrigacao.r` faz análise estatística dos dados coletados.

Para usar:

1. Abra o RStudio
2. Execute o script `analise_irrigacao.r`
3. Visualize as estatísticas e gráficos

## Resultados Esperados

O sistema monitora continuamente os sensores e toma decisões automáticas sobre irrigação, otimizando o uso de água e garantindo as condições ideais para o cultivo de café.

## Video Demonstrativo

[\[Link do vídeo no YouTube\]](https://youtu.be/rCiK4DYlnFY)

---

**Desenvolvido por:** Diego Filipe Pereira de Araujo
**RM:**
