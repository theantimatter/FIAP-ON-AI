import requests

# Coordenadas de Minas Gerais
latitude = -8.9667
longitude = -72.7833

# API Open-Meteo (não requer chave de API)
url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code&hourly=precipitation&forecast_days=1"

try:
    resposta = requests.get(url)
    dados = resposta.json()

    if resposta.status_code == 200:
        temperatura = dados["current"]["temperature_2m"]
        umidade = dados["current"]["relative_humidity_2m"]
        precipitacao_atual = dados["current"]["precipitation"]
        codigo_clima = dados["current"]["weather_code"]

        # Previsão de precipitação nas próximas horas
        precipitacao_horaria = dados["hourly"]["precipitation"]
        tem_previsao_chuva = any(p > 0 for p in precipitacao_horaria[:12])  # Próximas 12 horas

        print("=== Previsao do Tempo ===")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        print(f"Temperatura: {temperatura}°C")
        print(f"Umidade: {umidade}%")
        print(f"Precipitacao atual: {precipitacao_atual} mm")

        if precipitacao_atual > 0 or tem_previsao_chuva:
            print("\nALERTA: Previsao de chuva!")
            print("Recomendacao: Suspender irrigacao")
        else:
            print("\nSem previsao de chuva")
            print("Irrigacao pode ser mantida conforme sensores")
    else:
        print("Erro ao buscar dados do clima")

except Exception as e:
    print(f"Erro: {e}")
