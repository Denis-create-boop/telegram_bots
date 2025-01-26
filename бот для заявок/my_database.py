import mysql.connector
from datetime import datetime

SECRET_KEY = "some_key"

db = mysql.connector.connect(host='localhost', 
                            database='BotBase',
                            user='root',
                            password=SECRET_KEY,
                            use_pure=True
                            )
cursor = db.cursor()


class Applications:
    """Класс для работы с заявками в бд"""

    def __init__(self, user=None, application=None, status=None, user_id=None):
        self.user = user
        self.application = application
        self.status = status
        self.user_id = user_id

    # соеденение с базой данных  с помощью слова connect
    def write_application(self):

        # создание таблицы в бд
        query = """ CREATE TABLE IF NOT EXISTS applications(id INTEGER, дата VARCHAR(50), 
        время VARCHAR(50), номер INTEGER, логин VARCHAR(50), проблема VARCHAR(50), статус VARCHAR(50), 
        оценка INTEGER, user_id BIGINT, master_id BIGITN) """
        cursor.execute(query)
        db.commit()

        # получаем последний id из бд
        def get_id():
            query = """ SELECT MAX(id) FROM applications """
            cursor.execute(query)
            id = 0
            for row in cursor:
                if row[0] is None:
                    id = 1
                else:
                    id = int(row[0]) + 1
            return id

        # заполнение таблицы в бд
        def write(id, user, number, application, status, user_id):
            global cursor
            data = str(datetime.now()).split()
            day = data[0]
            time = data[1][:8]
            query = """INSERT INTO applications
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            insert_payments = (id, day, time, number, user, application, status, None, user_id, None)

            cursor.execute(query, insert_payments)

            # перед закрытием обязательно нужно закомитить
            db.commit()

        id = get_id()
        number = id

        write(id, self.user, number, self.application, self.status, self.user_id)

        return number

    # получаем все заявки за определенный период
    def show_all(self, month):
        query = """ SELECT * FROM applications WHERE MONTH(дата) = %s """
        cursor.execute(query, (month, ))
        return cursor

    # функция для закрепления заявки за мастером
    def set_master_id(self, number, id_master):
        query = """UPDATE applications SET master_id = %s WHERE номер = %s"""
        cursor.execute(query, (number, id_master,))
        db.commit()

    # функция для просмотра мастером своих заявок
    def get_master_applications(self, master_id, month):
        query = """SELECT * FROM applications WHERE master_id = %s AND MONTH(дата) = %s"""
        cursor.execute(query, (master_id, month,))
        return cursor


    # функция для получения оценки заявки
    def get_grade(self, number):

        query = """SELECT оценка FROM applications WHERE номер = %s"""
        cursor.execute(query, (number, ))
        for row in cursor:
            return row[0]

    # функция оценивания выполнения
    def set_grade(self, number, grade):

        query = """ UPDATE applications SET оценка = %s WHERE номер = %s """
        cursor.execute(
                query,
                (
                    grade,
                    number,
                ),
            )
        db.commit()

    # получаем id заказчика
    def get_user_id(self, number):

        query = """ SELECT user_id FROM applications WHERE номер = %s """
        cursor.execute(query, (number, ))
        for row in cursor:
            return row[0]

    # получаем статус заявки
    def get_status(self, number):

        query = """ SELECT статус FROM applications WHERE номер = %s """
        cursor.execute(query, (number, ))
        for row in cursor:
            return row

    # устанавливаем новый статус заявки
    def set_new_status(self, number, status):

        query = """ UPDATE applications SET статус = %s WHERE номер = %s """
        cursor.execute(
                query,
                (
                    status,
                    number,
                ),
            )
        db.commit()

    # получаем заявку
    def get_application(self, number):

        query = """ SELECT * FROM applications WHERE номер = %s """
        cursor.execute(query, (number, ))
        return cursor

    # удаляем заявку из бд
    def del_application(self, number):
        query = """ DELETE FROM applications WHERE номер = %s """
        cursor.execute(query, (number, ))
        db.commit()
