"""
alertas_aws.py — FarmTech Solutions (Fase 7)

Módulo de alertas via AWS SNS.
Pré-requisitos:
  pip install boto3
  aws configure   (ou variáveis de ambiente AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
"""

import boto3
from datetime import datetime


def enviar_alerta(topico_arn: str, mensagem: str, assunto: str, regiao: str = "us-east-1"):
    """Publica uma mensagem em um tópico SNS."""
    sns = boto3.client("sns", region_name=regiao)
    return sns.publish(TopicArn=topico_arn, Message=mensagem, Subject=assunto)


def alerta_umidade_critica(topico_arn: str, umidade_atual: float, limite: float = 40.0):
    """Dispara alerta quando a umidade do solo cai abaixo do limite (Fase 3)."""
    vol_estimado = (limite - umidade_atual) * 2
    mensagem = (
        f"ALERTA FARMTECH — Umidade Crítica\n\n"
        f"Timestamp    : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        f"Umidade atual: {umidade_atual:.1f}%\n"
        f"Limite crítico: {limite:.1f}%\n\n"
        f"Ação recomendada:\n"
        f"  - Ativar bomba de irrigação imediatamente\n"
        f"  - Aplicar ~{vol_estimado:.0f} L/ha\n"
        f"  - Monitorar nas próximas 2 horas\n\n"
        f"FarmTech Solutions — Sistema de Alertas Automáticos"
    )
    return enviar_alerta(topico_arn, mensagem, "[FarmTech] URGENTE: Umidade Crítica")


def alerta_ph_fora_faixa(topico_arn: str, ph_atual: float, ph_min: float = 6.0, ph_max: float = 8.0):
    """Dispara alerta quando o pH do solo sai da faixa ideal (Fase 3)."""
    acao = (
        "Aplicar calcário para elevar o pH"
        if ph_atual < ph_min
        else "Aplicar enxofre ou matéria orgânica para reduzir o pH"
    )
    mensagem = (
        f"ALERTA FARMTECH — pH Fora da Faixa\n\n"
        f"Timestamp : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        f"pH atual  : {ph_atual:.1f}\n"
        f"Faixa ideal: {ph_min} – {ph_max}\n\n"
        f"Ação recomendada:\n"
        f"  - {acao}\n"
        f"  - Refazer análise de solo em 30 dias\n\n"
        f"FarmTech Solutions — Sistema de Alertas Automáticos"
    )
    return enviar_alerta(topico_arn, mensagem, "[FarmTech] Alerta de pH")


def alerta_visao_computacional(topico_arn: str, score_saude: float, status: str):
    """Dispara alerta com base na análise de imagem da plantação (Fase 6)."""
    mensagem = (
        f"ALERTA FARMTECH — Visão Computacional\n\n"
        f"Timestamp   : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        f"Score Saúde : {score_saude:.0f}/100\n"
        f"Status      : {status}\n\n"
        f"Ação recomendada:\n"
        f"  - Realizar inspeção presencial na lavoura\n"
        f"  - Verificar presença de pragas ou doenças\n"
        f"  - Consultar agrônomo para diagnóstico\n\n"
        f"FarmTech Solutions — Sistema de Alertas Automáticos"
    )
    return enviar_alerta(topico_arn, mensagem, f"[FarmTech] Visão Computacional: {status}")


def alerta_irrigacao_urgente(topico_arn: str, volume_l_ha: float):
    """Dispara alerta quando o modelo ML indica necessidade urgente de irrigação (Fase 4)."""
    mensagem = (
        f"ALERTA FARMTECH — Irrigação Urgente (ML)\n\n"
        f"Timestamp        : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        f"Volume indicado  : {volume_l_ha:.0f} L/ha\n\n"
        f"Ação recomendada:\n"
        f"  - Ativar sistema de irrigação imediatamente\n"
        f"  - Verificar disponibilidade hídrica\n\n"
        f"FarmTech Solutions — Sistema de Alertas Automáticos"
    )
    return enviar_alerta(topico_arn, mensagem, "[FarmTech] URGENTE: Irrigação Necessária")


if __name__ == "__main__":
    print("Módulo de alertas AWS SNS — FarmTech Solutions (Fase 7)")
    print()
    print("Funções disponíveis:")
    print("  alerta_umidade_critica(topico_arn, umidade_atual)")
    print("  alerta_ph_fora_faixa(topico_arn, ph_atual)")
    print("  alerta_visao_computacional(topico_arn, score_saude, status)")
    print("  alerta_irrigacao_urgente(topico_arn, volume_l_ha)")
    print()
    print("Exemplo:")
    print("  from alertas_aws import alerta_umidade_critica")
    print("  alerta_umidade_critica('arn:aws:sns:us-east-1:123:farmtech', 35.0)")
