'''База данных для телеграмм Бота'''
import sqlite3
import os

# создаем файл БД, если его нет
if not os.path.exists('database.db'):
    my_file = open("database.db", "w+")
    my_file.close()

# заполнение продуктами БД
def zap_db(con):
    conn[1].execute("DELETE FROM Products") #почистим перед заполнением
    for i in range(1, 5):
        conn[1].execute("SELECT id FROM Products WHERE id=?", (i,))
        data = conn[1].fetchone()
        if data is None:
            conn[1].execute("INSERT INTO Products(title,description,price) VALUES(?,?,?)",
                           (f"Продукт №{i}", f"Описание продукта №{i}", f"{100 * i}"))

# подключение к БД
def connect_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    return connection, cursor

# создаем таблицы Products и Users
def initiate_db(conn):
    conn[1].execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL    
    )
    ''')
    conn[1].execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL    
    )
    ''')

# выводит все продукты из БД
def get_all_products(conn):
    conn[1].execute("SELECT * FROM Products ")
    products = conn[1].fetchall()
    return products

# выводит если username есть в БД
def is_included(conn,username):
    conn[1].execute("SELECT id FROM Users WHERE username=?", (username,))
    data = conn[1].fetchone()
    if data is None:
        return False
    else:
        return True

# добавить в БД нового user
def add_user(conn, username, email, age):
    if not is_included(conn,username):
        conn[1].execute("INSERT INTO Users(username,email,age,balance) VALUES(?,?,?,?)",
                    (username,email,age,1000))
        conn[0].commit()


if __name__ == '__main__':
    conn = connect_db() #подключаем БД
    initiate_db(conn) #создаем таблицу, если ее нет
    zap_db(conn) #заполняем таблицу данными
    products = get_all_products(conn) # выводим эти данные
    for product in products:
        print(f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}")

    conn[0].commit() # сохраняемся
    conn[0].close() # выходим