import uuid
from datetime import datetime


def gerar_id_unico():
    # Obter a data/hora atual
    data_hora_atual = datetime.now().strftime('%d%m%y%H%M%S')

    # Gerar um UUID aleatório
    # Remover os hífens para garantir que seja uma string
    uuid_aleatorio = str(uuid.uuid4()).replace('-', '')

    # Combinar a data/hora atual e o UUID
    id_unico = uuid_aleatorio + "$" + data_hora_atual

    return id_unico
