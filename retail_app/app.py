import os
import psycopg2
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

load_dotenv()

fk = Faker()

host = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "postgres")

def connect_db():
    conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
    )

    return conn, conn.cursor()

def insert_orders(cursor):
    order_items_query = """
        INSERT INTO orders (order_time, branch) 
        VALUES (%s, %s)
        RETURNING order_id
    """
    
    branch_elements = (
        'New York',
        'Los Angeles',
        'Chicago',
        'Houston',
        'Phoenix',
        'Philadelphia',
        'San Antonio',
        'San Diego',
        'Dallas',
        'San Jose',
        'Austin',
        'Jacksonville',
    )
    
    branch = fk.random_element(elements=branch_elements)
    order_time = datetime.now()
    
    cursor.execute(order_items_query, (order_time, branch))
    order_id = cursor.fetchone()[0]
    print(f"Order ID: {order_id}")
    
    return order_id

def insert_orders_histories(cursor, order_id):
    order_history_items_query = """
        INSERT INTO ordershistory (order_id, status, updated_at)
        VALUES (%s, %s, %s)
        RETURNING history_id
    """
    
    status_elements = (
        'new',
        'intransit',
        'delivered'
    )
    
    status = fk.random_element(elements=status_elements)
    updated_at = datetime.now()
    
    cursor.execute(order_history_items_query, (order_id, status, updated_at))
    history_id = cursor.fetchone()[0]
    print(f"Order History ID: {history_id}")
    
try:
    print('Inserting data...')
    print('-' * 50)
    sleep(1)
        
    for _ in range(1000):
        conn, cursor = connect_db()
        order_id = insert_orders(cursor)
        insert_orders_histories(cursor, order_id)
        print('-' * 50)
        
        conn.commit()
    
    print('Data inserted successfully!')
    
except psycopg2.Error as e:
    print(f"Erro ao conectar com banco de dados: {e}")
    
finally:
    conn.close()
