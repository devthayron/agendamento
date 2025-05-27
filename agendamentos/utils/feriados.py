import datetime

# Feriados fixos com nome
FERIADOS_FIXOS = {
    (1, 1): "Confraternização Universal",
    (4, 21): "Tiradentes",
    (5, 1): "Dia do Trabalho",
    (9, 7): "Independência do Brasil",
    (10, 12): "Nossa Senhora Aparecida",
    (11, 2): "Finados",
    (11, 15): "Proclamação da República",
    (12, 25): "Natal",
}

# Feriados variáveis com nome
FERIADOS_VARIAVEIS_2025 = {
    datetime.date(2025, 3, 4): "Carnaval",
    datetime.date(2025, 4, 18): "Sexta-feira Santa",
    datetime.date(2025, 4, 20): "Páscoa",
    datetime.date(2025, 6, 19): "Corpus Christi",
    # adiciona mais se precisar
}

def get_feriado_nome(data: datetime.date):
    # Verifica feriados fixos
    nome = FERIADOS_FIXOS.get((data.month, data.day))
    if nome:
        return nome
    
    # Verifica feriados variáveis
    nome = FERIADOS_VARIAVEIS_2025.get(data)
    if nome:
        return nome
    
    return None
