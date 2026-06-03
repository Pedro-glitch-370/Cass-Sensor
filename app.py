import os
import time
import uuid
import random

from cassandra.cluster import Cluster
from cassandra.cluster import NoHostAvailable

def conectar():
    host = os.environ.get('CASSANDRA_HOST', 'cassandra-db')
    print(f"Tentando conectar ao Cassandra em {host}...")
    while True:
        try:
            cluster = Cluster([host])
            session = cluster.connect()
            print("Conectado ao Cassandra com sucesso!")
            return session
        except NoHostAvailable:
            print("Cassandra ainda não está pronto... aguardando 5 segundos.")
            time.sleep(5)

# script para povoar o banco de dados
def povoar_tabela(session):
    session.set_keyspace('monitoramento_iot')
    print("Inserindo dados...")
    
    # Lista para salvar um ID e testar a busca individual depois
    ids_inseridos = []

    for i in range(20):
        id_leitura = uuid.uuid4()
        temperatura = round(random.uniform(20, 40), 2)

        query = """
        INSERT INTO leituras (id, temperatura)
        VALUES (%s, %s)
        """
        session.execute(query, (id_leitura, temperatura))
        ids_inseridos.append(id_leitura)

        print(f"Leitura {i+1} inserida -> ID: {id_leitura} | Temp: {temperatura}°C")
        time.sleep(0.5) # Reduzi um pouco para o teste rodar mais rápido
        
    return ids_inseridos

# --- CONSULTAS ---

def consultar_todas_leituras(session):
    print("\n=== CONSULTA 1: Todas as Leituras Registradas ===")
    query = "SELECT * FROM leituras"
    rows = session.execute(query)
    
    contador = 0
    for row in rows:
        print(f"ID: {row.id} | Temperatura: {row.temperatura}°C")
        contador += 1
    print(f"Total de registros encontrados: {contador}")


def consultar_temperaturas_altas(session, limite_temp):
    print(f"\n=== CONSULTA 2: Leituras com Temperatura Acima de {limite_temp}°C ===")
    
    # ALLOW FILTERING é necessário aqui se 'temperatura' não for uma chave de partição/indexada
    query = "SELECT * FROM leituras WHERE temperatura > %s ALLOW FILTERING"
    rows = session.execute(query, (limite_temp,))
    
    contador = 0
    for row in rows:
        print(f"Alerta! -> ID: {row.id} | Temperatura Crítica: {row.temperatura}°C")
        contador += 1
    if contador == 0:
        print("Nenhuma leitura acima do limite.")


def consultar_por_id(session, uuid_do_registro):
    print(f"\n=== CONSULTA BASE: Buscando registro específico ===")
    query = "SELECT * FROM leituras WHERE id = %s"
    rows = session.execute(query, (uuid_do_registro,))
    
    for row in rows:
        print(f"Resultado Encontrado -> ID: {row.id} | Temp: {row.temperatura}°C")


def main():
    session = conectar()
    
    # Altera para o keyspace correto antes de tudo
    session.set_keyspace('monitoramento_iot')

    # Povoa e colhe os IDs criados para teste
    ids = povoar_tabela(session)
    print("Banco povoado com sucesso!")

    # Executa a Consulta 1 (Tudo)
    consultar_todas_leituras(session)

    # Executa a Consulta 2 (Filtro por valor de negócio)
    consultar_temperaturas_altas(session, limite_temp=35.0)

    # Executa a sua consulta original usando o primeiro ID que foi gerado neste script
    if ids:
        consultar_por_id(session, ids[0])

if __name__ == "__main__":
    main()