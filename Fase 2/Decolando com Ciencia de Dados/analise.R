# DiegoFilipePereiraDeAraujo_RM567064_fase2_cap8

dados <- read.csv("dados_producao_agricola.csv")

producao <- dados$producao

media <- mean(producao)
mediana <- median(producao)
moda <- function(x) {
  tabela <- table(x)
  as.numeric(names(tabela[tabela == max(tabela)]))
}
valor_moda <- moda(producao)

variancia <- var(producao)
desvio_padrao <- sd(producao)
amplitude <- max(producao) - min(producao)
coeficiente_variacao <- (desvio_padrao / media) * 100

quartis <- quantile(producao)
q1 <- quartis[2]
q2 <- quartis[3]
q3 <- quartis[4]
amplitude_interquartil <- q3 - q1

print("ANALISE DA PRODUCAO AGRICOLA")
print("=============================")
print("")
print("MEDIDAS DE TENDENCIA CENTRAL")
print(paste("Media:", media))
print(paste("Mediana:", mediana))
print(paste("Moda:", valor_moda[1]))
print("")
print("MEDIDAS DE DISPERSAO")
print(paste("Variancia:", variancia))
print(paste("Desvio Padrao:", desvio_padrao))
print(paste("Amplitude:", amplitude))
print(paste("Coeficiente de Variacao:", coeficiente_variacao, "%"))
print("")
print("MEDIDAS SEPARATRIZES")
print(paste("Q1:", q1))
print(paste("Q2:", q2))
print(paste("Q3:", q3))
print(paste("Amplitude Interquartil:", amplitude_interquartil))

par(mfrow=c(2,2))

hist(producao,
     main="Histograma da Producao",
     xlab="Producao (toneladas)",
     ylab="Frequencia",
     col="lightblue")

boxplot(producao,
        main="Boxplot da Producao",
        ylab="Producao (toneladas)",
        col="lightgreen")

plot(producao,
     main="Dispersao da Producao",
     xlab="Observacao",
     ylab="Producao (toneladas)",
     col="blue",
     pch=19)

densidade <- density(producao)
plot(densidade,
     main="Densidade da Producao",
     xlab="Producao (toneladas)",
     ylab="Densidade",
     col="red",
     lwd=2)

cultura <- dados$cultura

tabela_cultura <- table(cultura)

barplot(tabela_cultura,
        main="Distribuicao por Cultura",
        xlab="Cultura",
        ylab="Frequencia",
        col=rainbow(length(tabela_cultura)),
        las=2)

pie(tabela_cultura,
    main="Proporcao de Culturas",
    col=rainbow(length(tabela_cultura)))
