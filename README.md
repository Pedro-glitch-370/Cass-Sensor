# Cass-Sensor
Caso de Uso de Sistema de Log de Sensores IoT

Este projeto demonstra uma integração simples entre uma aplicação Python e um banco de dados NoSQL **Apache Cassandra**, utilizando **Docker** para padronização do ambiente.

## Pré-requisitos
* Docker e Docker Compose instalados.

## Como rodar o projeto

1. **Subir o ambiente:**
   No diretório raiz do projeto, execute o comando abaixo para iniciar o banco de dados e a aplicação em segundo plano:
   ```bash
   docker compose up -d
   ```
   O container da aplicação (app-integracao) irá rodar o script Python e criar automaticamente o Keyspace e a tabela.

2. **Verificar os dados:**
   Após a subida dos containers, você pode acessar o shell do Cassandra para consultar os dados inseridos pelo script:
   ```bash
   docker exec -it cassandra-db cqlsh
   ```

3. **Consultar os dados:**
   Uma vez dentro do terminal do Cassandra, execute os comandos:
   ```sql
   USE monitoramento_iot;
   SELECT * FROM leituras;
   ```

4. **Encerrar o ambiente:**
   Para parar e remover os containers e redes criadas, utilize:
   ```bash
   docker compose down
   ```

Este ambiente garante que a integração ocorra de forma isolada, sem depender de configurações manuais ou versões de Python instaladas na máquina hospedeira.