import sqlite3


class Table:
    """Класс для работы с заявками в бд"""
    def __init__(self, user=None, question=None, status=None, user_id=None):
        self.user = user
        self.question = question
        self.status = status
        self.user_id = user_id

    # соеденение с базой данных  с помощью слова connect
    def write_question(self):
        with sqlite3.connect('./database.db') as db:

            # создание таблицы в бд
            cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS questions(id INTEGER, номер INTEGER, логин TEXT, проблема TEXT, статус TEXT, оценка INTEGER, user_id INTEGER) """
            cursor.execute(query)

            # получаем последний id из бд
            def get_id():
                query = """ SELECT MAX(id) FROM questions """
                cursor.execute(query)
                id = 0
                for row in cursor:
                    if row[0] is None:
                        id = 1
                    else:
                        id = int(row[0]) + 1
                return id

            # заполнение таблицы в бд
            def write(id, user, number, question, status, user_id):

                cursor = db.cursor()
                query = """ INSERT INTO questions(id, номер, логин, проблема, статус, user_id) VALUES(?, ?, ?, ?, ?, ?) """
                insert_payments = [(id, number, user, question, status, user_id)]
                cursor.executemany(query, insert_payments)

                # перед закрытием обязательно нужно закомитить
                db.commit()
            id = get_id()
            number = id

            write(id, self.user, number, self.question, self.status, self.user_id)

            return number

    # получаем все заявки
    def show_all(self):
        with sqlite3.connect('./database.db') as db:

            cursor = db.cursor()
            query = """ SELECT * FROM questions """
            cursor.execute(query)
            return cursor

    # функция для получения оценки заявки
    def get_grade(self, number):
        with sqlite3.connect("./database.db") as db:

            cursor = db.cursor()
            query = f""" SELECT оценка FROM questions WHERE номер == {number}"""
            cursor.execute(query)
            for row in cursor:
                return row[0]

    # функция оценивания выполнения
    def set_grade(self, number, grade):
        with sqlite3.connect("./database.db") as db:

            cursor = db.cursor()
            query = """ UPDATE questions SET оценка = ? WHERE номер == ? """
            cursor.executemany(
                query,
                [
                    (
                        grade,
                        number,
                    )
                ],
            )
            db.commit()

    # получаем id заказчика
    def get_user_id(self, number):
        with sqlite3.connect("./database.db") as db:

            cursor = db.cursor()
            query = f""" SELECT user_id FROM questions WHERE номер == {number} """
            cursor.execute(query)
            for row in cursor:
                return row[0]
            

    # получаем статус заявки
    def get_status(self, number):
        with sqlite3.connect('./database.db') as db:

            cursor = db.cursor()
            query = f""" SELECT статус FROM questions WHERE номер == {number} """
            cursor.execute(query)
            for row in cursor:
                return row

    # устанавливаем новый статус заявки
    def set_new_status(self, number, status):
        with sqlite3.connect('./database.db') as db:

            cursor = db.cursor()
            query = """ UPDATE questions SET статус = ? WHERE номер == ? """
            cursor.executemany(query, [(status, number,)])
            db.commit()

    # получаем заявку
    def get_question(self, number):
        with sqlite3.connect('./database.db') as db:

            cursor = db.cursor()
            query = f""" SELECT * FROM questions WHERE номер == {number} """
            cursor.execute(query)
            return cursor

    # удаляем заявку из бд
    def del_question(self, number):
        with sqlite3.connect('./database.db') as db:

            cursor = db.cursor()
            query = f""" DELETE FROM questions WHERE номер == {number} """
            cursor.execute(query)
            db.commit()
