import oracledb

# Параметри за връзка с Oracle база данни
username = 'вашето_потребителско_име'
password = 'вашата_парола'
dsn = 'ваш_dsn'  # Името на Oracle Database
port = 'ваш_порт'  # Порт (например, 1521)
encoding = 'UTF-8'  # Кодировка

# Създаване на връзка с базата данни
connection = oracledb.connect(username, password, f'{dsn}:{port}/{username}', encoding=encoding)

# Създаване на курсор
cursor = connection.cursor()

# Изпълнение на SELECT заявка
query = 'SELECT * FROM вашата_таблица'
cursor.execute(query)

# Извличане на резултатите
for row in cursor.fetchall():
    print(row)

# Затваряне на курсора и връзката
cursor.close()
connection.close()
