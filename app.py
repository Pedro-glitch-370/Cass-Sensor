import os
import time
from cassandra.cluster import Cluster
from cassandra.cluster import NoHostAvailable

def main():
    host = os.environ.get('CASSANDRA_HOST', 'cassandra-db')
    
    print(f"Tentando conectar ao Cassandra em {host}...")
    
    # Loop de tentativa de conexão
    while True:
        try:
            cluster = Cluster([host])
            session = cluster.connect()
            print("Conectado ao Cassandra com sucesso!")
            break # Sai do loop se conectar
        except NoHostAvailable:
            print("Cassandra ainda não está pronto... aguardando 5 segundos.")
            time.sleep(5)

    # Criar Keyspace e Tabela
    session.execute("CREATE KEYSPACE IF NOT EXISTS monitoramento_iot WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")
    session.set_keyspace('monitoramento_iot')
    session.execute("CREATE TABLE IF NOT EXISTS leituras (id uuid PRIMARY KEY, temperatura float)")
    
    print("Tabela pronta!")

if __name__ == "__main__":
    main()