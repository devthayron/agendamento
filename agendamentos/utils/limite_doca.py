from datetime import timedelta
from agendamentos.models import Agendamento

LIMITES_DOCAS = {
    'galpao1': 1,
    'galpao2': 3,
    'galpao3': 3,
    'galpao4': 2,
}

def verificar_disponibilidade(galpao, data_agendamento, agendamento_id=None, sem_limite_doca=False):
    if not galpao or sem_limite_doca:
        return True, None

    limite = LIMITES_DOCAS.get(galpao, 0)
    agendamentos_do_dia = Agendamento.objects.filter(
        galpao=galpao,
        data_hora__date=data_agendamento
    )

    # Exclui o próprio agendamento em caso de edição
    if agendamento_id:
        agendamentos_do_dia = agendamentos_do_dia.exclude(id=agendamento_id)

    if agendamentos_do_dia.count() < limite:
        return True, None  # Disponível
    
    # Verifica datas anteriores e posteriores
    dias_busca = 7
    data_anterior = data_agendamento - timedelta(days=1)
    data_posterior = data_agendamento + timedelta(days=1)

    data_disponivel_anterior = None
    data_disponivel_posterior = None

    for _ in range(dias_busca):
        if not data_disponivel_anterior:
            ags_ant = Agendamento.objects.filter(galpao=galpao, data_hora__date=data_anterior)
            if agendamento_id:
                ags_ant = ags_ant.exclude(id=agendamento_id)
            if ags_ant.count() < limite:
                data_disponivel_anterior = data_anterior

        if not data_disponivel_posterior:
            ags_post = Agendamento.objects.filter(galpao=galpao, data_hora__date=data_posterior)
            if agendamento_id:
                ags_post = ags_post.exclude(id=agendamento_id)
            if ags_post.count() < limite:
                data_disponivel_posterior = data_posterior

        if data_disponivel_anterior and data_disponivel_posterior:
            break

        data_anterior -= timedelta(days=1)
        data_posterior += timedelta(days=1)

    return False, {
        "mensagem": f"Limite de agendamentos atingido para {galpao} em {data_agendamento.strftime('%d/%m/%Y')}.",
        "anterior": data_disponivel_anterior.strftime('%d/%m/%Y') if data_disponivel_anterior else None,
        "posterior": data_disponivel_posterior.strftime('%d/%m/%Y') if data_disponivel_posterior else None,
    }

