import mysql.connector
import configparser
import pandas as pd
from mysql.connector import Error

#return connection to sql
def create_connection(host_name, user_name, user_password,db):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db
        )
        #print("connected to db")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

#Function to run SQL query. Pass function from map_data.py return results of util function.   
def get_connection():
    #get sql credentials from config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    host=config.get('mysql','host')
    username=config.get('mysql','username')
    password=config.get('mysql','password')
    database=config.get('mysql','db')

    #connect to database
    connection=create_connection(host,username,password,database)

    return(connection)

def get_login(connection,username,password):
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM login WHERE username= %s AND password = %s", (username, password,))
    account=cursor.fetchone()
    return(account)

def get_menu(connection):
    #inner class for food item
    class __item__:
        def __init__(self,number,item,price):
            self.number = number
            self.item = item
            self.price=price
    
    combos_df = pd.read_sql('SELECT * FROM combo',connection)
    pizzas_df = pd.read_sql('SELECT * FROM pizza',connection)
    sides_df = pd.read_sql('SELECT * FROM sides',connection)
    subs_df = pd.read_sql('SELECT * FROM subs',connection)

    combos = []
    for row in combos_df.itertuples():
        combos.append(__item__(row[1],row[2],row[3]))

    pizzas = []
    for row in pizzas_df.itertuples():
        pizzas.append(__item__(row[1],row[2],row[3]))

    sides = []
    for row in sides_df.itertuples():
        sides.append(__item__(row[1],row[2],row[3]))

    subs = []
    for row in subs_df.itertuples():
        subs.append(__item__(row[1],row[2],row[3]))
    

    return (combos,pizzas,sides,subs)

def send_order(connection,order):
    cursor=connection.cursor(dictionary=True)
    cursor.execute('INSERT INTO `orders` (`cus_order`, `paid`) VALUES (%s, %s)',(order,'Paid by Credit Card',))
    connection.commit()
    
