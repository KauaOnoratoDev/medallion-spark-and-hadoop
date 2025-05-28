import os
import psycopg2
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import sleep
from random import randint, gauss

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
    
    return order_id, order_time

def insert_orders_histories(cursor, order_id, initial_order_time):
    order_history_items_query = """
        INSERT INTO ordershistory (order_id, status, updated_at)
        VALUES (%s, %s, %s)
        RETURNING history_id
    """
     
    # 1. Inserir status 'new'
    cursor.execute(order_history_items_query, (order_id, 'new', initial_order_time))
    print(f"Order History ID: {cursor.fetchone()[0]} - Status: new")

    current_time = initial_order_time 
    minutes_time = randint(0, 59)
    hours_time = randint(0, 23)

    # 2. 75% chance de inserir status 'intransit'
    if randint(0, 3): 
        delay_days_intransit = gauss(5, 3)
        delay_days_intransit = max(1, delay_days_intransit)
        
        current_time += timedelta(days=delay_days_intransit, hours=hours_time, minutes=minutes_time)
        cursor.execute(order_history_items_query, (order_id, 'intransit', current_time))
        print(f"Order History ID: {cursor.fetchone()[0]} - Status: intransit")

        # 3. 50% chance de inserir status 'delivered' após o status 'intransit'	
        if randint(0, 1):
            delay_days_delivered = gauss(10, 5)
            delay_days_delivered = max(1, delay_days_delivered)
            
            current_time += timedelta(days=delay_days_delivered, hours=hours_time, minutes=minutes_time)
            cursor.execute(order_history_items_query, (order_id, 'delivered', current_time))
            print(f"Order History ID: {cursor.fetchone()[0]} - Status: delivered")
    
try:
    print('Inserting data...')
    print('-' * 50)
    sleep(1)
        
    for _ in range(1000):
        conn, cursor = connect_db()
        order_id, order_time = insert_orders(cursor)
        insert_orders_histories(cursor, order_id, order_time)
        print('-' * 50)
        
        conn.commit()
    
    print('Data inserted successfully!')
    
except psycopg2.Error as e:
    print(f"Erro ao conectar com banco de dados: {e}")
    
finally:
    conn.close()
