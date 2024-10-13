from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
from google.api_core.exceptions import NotFound
import os
from dotenv import load_dotenv

# Carregando as variáveis de ambiente
load_dotenv()

# Definindo o caminho para o arquivo de credenciais
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Criando o cliente
client = bigquery.Client()

# Definindo o ID do projeto e o nome do banco de dados
projeto_id = 'projeto-bigquery-airbyte'
db_id = 'dw_comercial'

# Definindo as propriedades do banco de dados
db_ref = client.dataset(db_id)
db = bigquery.Dataset(db_ref)

# Definindo a localização do banco de dados
db.location = 'US'

# Criando o banco de dados e as tabelas no BigQuery
try:
    db = client.create_dataset(db, exists_ok=True)
    print('Banco de dados criado com sucesso!')

    # Definindo os nomes e esquemas das tabelas
    tables_and_schemas = {
        'dim_clientes': [
            SchemaField('ID_Cliente', 'INTEGER', mode='REQUIRED'),
            SchemaField('Nome_Cliente', 'STRING', mode='REQUIRED'),
            SchemaField('Sobrenome_Cliente', 'STRING', mode='REQUIRED'),
            SchemaField('Data_Nascimento_Cliente', 'DATE', mode='REQUIRED'),
            SchemaField('CPF_Cliente', 'STRING', mode='REQUIRED'),
            SchemaField('Sexo_Cliente', 'STRING', mode='REQUIRED'),
            SchemaField('Email_Cliente', 'STRING', mode='NULLABLE'),
            SchemaField('Telefone_Cliente', 'STRING', mode='NULLABLE'),
            SchemaField('ID_Localidade', 'INTEGER', mode='REQUIRED')
        ],
        'dim_produtos': [
            SchemaField('ID_Produto', 'INTEGER', mode='REQUIRED'),
            SchemaField('Nome_Produto', 'STRING', mode='REQUIRED'),
            SchemaField('Categoria_Produto', 'STRING', mode='REQUIRED'),
            SchemaField('Subcategoria_Produto', 'STRING', mode='REQUIRED'),
            SchemaField('Custo_Unitario', 'FLOAT', mode='REQUIRED'),
            SchemaField('Preco', 'FLOAT', mode='REQUIRED')
        ],
        'dim_vendedores': [
            SchemaField('ID_Vendedor', 'INTEGER', mode='REQUIRED'),
            SchemaField('Nome_Vendedor', 'STRING', mode='REQUIRED'),
            SchemaField('Idade_Vendedor', 'INTEGER', mode='REQUIRED'),
            SchemaField('CPF_Vendedor', 'STRING', mode='REQUIRED'),
            SchemaField('Data_Nascimento_Vendedor', 'DATE', mode='REQUIRED'),
            SchemaField('Sexo_Vendedor', 'STRING', mode='REQUIRED'),
            SchemaField('Loja_Que_Trabalha', 'INTEGER', mode='REQUIRED')
        ],
        'dim_localidades': [
            SchemaField('ID_Localidade', 'INTEGER', mode='REQUIRED'),
            SchemaField('Rua_Cliente', 'STRING', mode='REQUIRED'),
            SchemaField('Numero_Cliente', 'INTEGER', mode='REQUIRED'),
            SchemaField('Bairro_Cliente', 'STRING', mode='REQUIRED'),
            SchemaField('Estado_Cliente', 'STRING', mode='REQUIRED'),
            SchemaField('Pais_Cliente', 'STRING', mode='REQUIRED')
        ],
        'dim_tempo': [
            SchemaField('ID_Tempo', 'INTEGER', mode='REQUIRED'),
            SchemaField('Dia', 'INTEGER', mode='REQUIRED'),
            SchemaField('Mes', 'INTEGER', mode='REQUIRED'),
            SchemaField('Mes_Abreviado', 'STRING', mode='REQUIRED'),
            SchemaField('Ano', 'INTEGER', mode='REQUIRED'),
            SchemaField('Mes_Ano', 'STRING', mode='REQUIRED'),
            SchemaField('Dia_da_Semana', 'STRING', mode='REQUIRED'),
            SchemaField('Final_de_Semana', 'STRING', mode='REQUIRED')
        ],
        'dim_lojas': [
            SchemaField('ID_Loja', 'INTEGER', mode='REQUIRED'),
            SchemaField('Nome_Loja', 'STRING', mode='REQUIRED')
        ],
        'fato_vendas': [
            SchemaField('ID_Venda', 'INTEGER', mode='REQUIRED'),
            SchemaField('ID_Produto', 'INTEGER', mode='REQUIRED'),
            SchemaField('ID_Cliente', 'INTEGER', mode='REQUIRED'),
            SchemaField('ID_Tempo', 'INTEGER', mode='REQUIRED'),
            SchemaField('ID_Vendedor', 'INTEGER', mode='REQUIRED'),
            SchemaField('ID_Loja', 'INTEGER', mode='REQUIRED'),
            SchemaField('Quantidade_Produto', 'INTEGER', mode='REQUIRED'),
            SchemaField('Preco_Total', 'FLOAT', mode='REQUIRED')
        ]
    }

    # Criando as tabelas
    for table_name, schema in tables_and_schemas.items():
        table_ref = db_ref.table(table_name)
        
        try:
            client.get_table(table_ref)
            print(f'A tabela {table_name} já existe no banco de dados')
        except NotFound:
            table = bigquery.Table(table_ref, schema=schema)
            table = client.create_table(table)
            print(f'Tabela {table_name} criada com sucesso!')
        except Exception as e:
            print(f'Erro ao criar a tabela {table_name}: {e}')

except Exception as e:
    print(f'Erro ao criar o banco de dados: {e}')
