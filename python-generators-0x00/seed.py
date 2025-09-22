
import mysql.connector
import csv
import uuid

DB_NAME = "ALX_prodev"

def connect_db():
    """Connect to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create database if not exists"""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    connection.commit()

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to {DB_NAME}: {e}")
        return None

def create_table(connection):
    """Create user_data table"""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """)
    cursor.close()
    connection.commit()
    print("Table user_data created successfully")

def insert_data(connection, csv_file):
    """Insert CSV data into table"""
    cursor = connection.cursor()
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (str(uuid.uuid4()), row['name'], row['email'], int(row['age'])))
    cursor.close()
    connection.commit()
    print("Data inserted successfully")
