umidade_solo <- c(45, 52, 38, 61, 55, 48, 42, 59, 50, 44, 47, 53, 40, 58, 49)
ph_solo <- c(6.2, 6.5, 5.8, 6.8, 6.3, 6.1, 5.9, 6.7, 6.4, 6.0, 6.2, 6.6, 5.7, 6.9, 6.3)

print("=== Analise de Umidade do Solo ===")
media_umidade <- mean(umidade_solo)
desvio_umidade <- sd(umidade_solo)

print(paste("Media de umidade:", round(media_umidade, 2), "%"))
print(paste("Desvio padrao:", round(desvio_umidade, 2), "%"))

if(media_umidade < 60) {
  print("Decisao: LIGAR bomba de irrigacao")
} else {
  print("Decisao: DESLIGAR bomba de irrigacao")
}

print("")
print("=== Analise de pH do Solo ===")
media_ph <- mean(ph_solo)
desvio_ph <- sd(ph_solo)

print(paste("Media de pH:", round(media_ph, 2)))
print(paste("Desvio padrao:", round(desvio_ph, 2)))

if(media_ph >= 5.5 & media_ph <= 7.0) {
  print("pH adequado para cultura de cafe")
} else {
  print("pH fora do ideal")
}

print("")
print("=== Graficos ===")

hist(umidade_solo, main="Distribuicao de Umidade do Solo", xlab="Umidade (%)", ylab="Frequencia", col="lightblue")

hist(ph_solo, main="Distribuicao de pH do Solo", xlab="pH", ylab="Frequencia", col="lightgreen")
