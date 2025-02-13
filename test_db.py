from db_module import *


sqlite_conn = DBConnector('sqlite')
schema = DBSchema(sqlite_conn)

for table,params in tables.items():
    if schema.create_table(table,params):
        print(f"Создание {table} прошло успешно")
    else:
        print(f"Ошибка создания {table}")
