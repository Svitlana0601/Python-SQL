import mysql.connector
# база данных для записи запросов
dbconfig_insert = {'host': 'ich-edit.edu.itcareerhub.de',
            'user': 'ich1',
            'password': 'ich1_password_ilovedbs',
            'port': 3306,
             'database': 'project_130524_svitlana_u'}
# база данных для извлечения информации
dbconfig_select = {'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
                    'user': 'ich1',
                    'password': 'password',
                    'database': 'sakila'}


def make_connection_to_sakila():
    connection = mysql.connector.connect(**dbconfig_select)
    cursor = connection.cursor()
    return connection, cursor

def make_connection_insert_ich():
    connection = mysql.connector.connect(**dbconfig_insert)
    cursor = connection.cursor()
    return connection, cursor

def make_close(connection, cursor):
    cursor.close()
    connection.close()

