import psycopg2
import os
'''
DB_CONFIG = {
    'dbname': 'postgres',  # o 'bertDirection' si la creas
   'user': 'adminAddress',
    'password': 'Familiacruz01.', 
    'host': 'postgres-tesis3.cbi4kw4gkfmm.us-east-2.rds.amazonaws.com',
    'port': '5432'
}
'''
'''
DB_CONFIG = {
   'dbname': 'bertDirection',
   'user': 'postgres',
   'password': 'host',
   'host': 'localhost',
   'port': '5432'
}
'''

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'bertDirection'),
    'user': os.getenv('DB_USER', 'pgadmin'),
    'password': os.getenv('DB_PASSWORD', 'Benja26...'),
    'host': os.getenv('DB_HOST', 'bert-direction.postgres.database.azure.com'),
    'port': os.getenv('DB_PORT', '5432')
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)