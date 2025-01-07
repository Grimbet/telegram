import sqlite3
import os

# создадим файл под базу данных
if not os.path.exists('not_telegram.db'):
    my_file = open("not_telegram.db", "w+")
    my_file.close()


#подключаем созданный файл БД
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
# создаем таблицу Users в БД со столбцами id,username,email,age,balance
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# очищаем таблицу (для многократного правильного запуска модуля)
# если не почистим, то будут добавляться удаленные строки
cursor.execute("DELETE FROM Users")

# заполняем таблицу в виде <User1, example1@gmail.com, 10, 1000>
# предварительно сделаем проверку, а нет ли уже такой записи, чтобы не дублировать (хотя незачем - просто пробуем)
for i in range(1,11):
    cursor.execute("SELECT id FROM Users WHERE id=?", (i,))
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO Users(username,email,age,balance) VALUES(?,?,?,?)",(f"User{i}",f"example{i}@gmail.com",f"{10*i}","1000") )

# получаем список Users для дальнейшей работы с ним
cursor.execute("SELECT * FROM Users")
users = cursor.fetchall()

# обновляем баланс у каждого второго с 1000 на 500, начиная с 1 (step=2)
for i in range(1,11,2):
    cursor.execute("UPDATE Users SET balance=? WHERE id=?", (500, i))

# удалим каждого третьего из БД, начиная с 1 (step=3)
for i in range(1,11,3):
    cursor.execute("DELETE FROM Users WHERE id=?", (i,))


 # Домашняя работа 14.2

# удалим user с id = 6
cursor.execute("DELETE FROM Users WHERE id=?", (6,))

# выводим итоги наших манипуляций
cursor.execute("SELECT * FROM Users WHERE age!=?", (60,))
users = cursor.fetchall()
for user in users:
    print(f"Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}")



#посчитаем кол-во записей в БД
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]
print(f"Всего в БД пользоватлей: {total_users}")
#  посчитаем сумму балансов всех пользователей БД
cursor.execute("SELECT SUM(balance) FROM Users ")
all_balance = cursor.fetchone()[0]
print(f"Общий баланс всех пользователей: {all_balance}")
# выведем средний баланс
print(f"Средний баланс БД: {all_balance/total_users}")
# сохраняемся и закрываем
connection.commit()
connection.close()
