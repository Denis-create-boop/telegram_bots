import telebot
from my_database import Applications
from telebot.types import InputMediaPhoto


TOKEN = "8018531675:AAHnItWE4t-ujEqPFe-0vCaFggdeY017re0"
bot = telebot.TeleBot(TOKEN)


id_admin = 5276576528
user_id = None
old_number = 0

admin_buttons = [
    "start",
    "👁Посмотреть все заявки👁",
    "изменить статус заявки",
    "удалить заявку",
    "посмотреть оценку заявки",
    "📩Не могу зайти в почту📩",
    "☁️Не могу зайти на портал☁️",
    "Не работает комп🤬🤬",
    "🔥🔥🤯Очень срочно ничего не работает🤯🔥🔥",
    "Другое",
    "Посмотреть статус заявки👀",
]

user_buttons = [
    "start",
    "📩Не могу зайти в почту📩",
    "☁️Не могу зайти на портал☁️",
    "Не работает комп🤬🤬",
    "🔥🔥🤯Очень срочно ничего не работает🤯🔥🔥",
    "Другое",
    "Посмотреть статус заявки👀",
]

user_handlers = [
    "start",
    "📩Не могу зайти в почту📩",
    "☁️Не могу зайти на портал☁️",
    "Не работает комп🤬🤬",
    "🔥🔥🤯Очень срочно ничего не работает🤯🔥🔥",
    "Другое",
]

master_buttons = [
    "start",
    "посмотреть свои заявки",
    "Заявку выполнил",
    "Передал заявку другому специалисту",
    "Невозможно решить проблему",
]

master_handlers = [
    "start",
    "посмотреть свои заявки",
    "Заявку выполнил",
    "Передал заявку другому специалисту",
    "Невозможно решить проблему",
]

seves_problems = {
    "start": "start",
    "👁Посмотреть все заявки👁": "Посмотреть все заявки",
    "изменить статус заявки": "изменить статус заявки",
    "удалить заявку": "удалить заявку",
    "посмотреть оценку заявки": "посмотреть оценку заявки",
    "📩Не могу зайти в почту📩": "Не могу зайти в почту",
    "☁️Не могу зайти на портал☁️": "Не могу зайти на портал",
    "Не работает комп🤬🤬": "Не работает комп",
    "🔥🔥🤯Очень срочно ничего не работает🤯🔥🔥": "Очень срочно ничего не работает",
    "Другое": "Другое",
    "Посмотреть статус заявки👀": "Посмотреть статус заявки",
    "Заявку выполнил": "Заявку выполнил",
    "Передал заявку другому специалисту": "Передал заявку другому специалисту",
    "Невозможно решить проблему": "Невозможно решить проблему",
}

# admin
def admin(message):

    @bot.message_handler(
        func=lambda message: str(message.text).lower() == "start"
        or message.text == "/start"
    )
    def wellcome(message):

        global admin_buttons, photo
        chat_id = message.chat.id
        keyboard = telebot.types.ReplyKeyboardMarkup()

        for button in admin_buttons:
            button_save = telebot.types.InlineKeyboardButton(text=button)
            keyboard.add(button_save)
        with open("images/avatar_main.jpg", "rb") as photo:
            bot.send_media_group(chat_id, [InputMediaPhoto(photo)])
        bot.send_message(
            chat_id,
            "Добро пожаловать в бот ДВП Воронеж ЦО",
            reply_markup=keyboard
        )

    # функция для просмотра оценки заявки
    @bot.message_handler(
        func=lambda message: message.text == "посмотреть оценку заявки"
    )
    def show_drade(message):
        chat_id = message.chat.id

        def get_number(message):
            bot.send_message(chat_id, "Введите номер заявки")
            bot.register_next_step_handler(message, get_grade)

        def get_grade(message):
            number = message.text
            objects = Applications()
            grade = objects.get_grade(number)
            bot.send_message(chat_id, f"Оценка заявки под номером {number} - {grade}")

        get_number(message)

    # функция для просмотра всех заявок
    @bot.message_handler(func=lambda message: message.text == "👁Посмотреть все заявки👁")
    def show_all(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "Выберите месяц за который хотите посмотреть заявки")
        bot.register_next_step_handler(message, show_for_month)

    def show_for_month(message):
        chat_id = message.chat.id
        month = message.text
        try:
            objects = Applications()
            objects = objects.show_all(month)
            ls_answer = ["id", "дата", "время", "номер заявки", "логин", "проблема", "статус", "оценка", "пользователь", "id_master"]
            ls_send = []
            for row in objects:
                send = ""
                for i in range(len(ls_answer)):
                    send += f"{ls_answer[i]}: {row[i]}\n"
                ls_send.append(send)
            for i in ls_send:
                bot.send_message(chat_id, i)
        except:
            bot.send_message(chat_id, "В базе данных за этот месяц нет ниодной заявки")

    # функция для изменения статуса заявки
    @bot.message_handler(func=lambda message: message.text == "изменить статус заявки")
    def change_status(message):
        global old_number
        chat_id = message.chat.id
        objects = Applications()
        old_status = ""

        status_buttons = [
            "В работе",
            "Передана специалисту",
            "Выполнена",
            "Невозможно решить проблему",
        ]
        keyboard = telebot.types.ReplyKeyboardMarkup()
        for button in status_buttons:
            button_save = telebot.types.InlineKeyboardButton(text=button)
            keyboard.add(button_save)

        def get_number(message):
            bot.send_message(chat_id, "Введите номер заявки")
            bot.register_next_step_handler(message, check_status)

        def check_status(message):
            global old_status, old_number
            NUM = message.text
            checks_status = objects.get_status(int(NUM))
            if checks_status[0] == "Выполнена":
                bot.send_message(
                    chat_id,
                    "Вы не можете изменить статус у этой заявки так как она уже выполнена",
                )
            else:
                num = message.text
                old_number = num
                old_status = objects.get_status(num)
                bot.send_message(chat_id, "Укажите статус заявки", reply_markup=keyboard)
                bot.register_next_step_handler(message, set_new_status)

        def set_new_status(message):
            global admin_buttons, user_id, old_number, old_status
            nonlocal objects

            new_keyboard = telebot.types.ReplyKeyboardMarkup()
            for button in admin_buttons:
                button_save = telebot.types.InlineKeyboardButton(text=button)
                new_keyboard.add(button_save)

            new_status = message.text
            objects.set_new_status(old_number, new_status)
            user_id = objects.get_user_id(old_number)
            bot.send_message(
                chat_id,
                f"Статус заявки номер {old_number}\nИзменен с:\n{old_status[0]}\nна:\n{new_status}",
                reply_markup=new_keyboard,
            )

            if new_status == "Выполнена":
                user_id = objects.get_user_id(old_number)
                grade_keyboard = telebot.types.ReplyKeyboardMarkup()
                grade_buttons = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
                for button in grade_buttons:
                    button_save = telebot.types.InlineKeyboardButton(text=button)
                    grade_keyboard.add(button_save)
                bot.send_message(
                    user_id,
                    f"Ваша заявка под номером {old_number} - Выполнена\nПожалуйста оцените качество работы от 1 до 10",
                    reply_markup=grade_keyboard,
                )

        get_number(message)

    @bot.message_handler(func=lambda message: message.text == "удалить заявку")
    # функция для удаления заявки из бд
    def delete_questions(message):
        number = 0
        objects = Applications()

        def start_delete(message):
            chat_id = message.chat.id
            bot.send_message(chat_id, "Введите номер заявки")
            bot.register_next_step_handler(message, answer_are_ready)

        def answer_are_ready(message):
            nonlocal number, objects
            chat_id = message.chat.id
            number = message.text
            answer_bd = objects.get_application(number)
            ls_answer = []
            for row in answer_bd:
                ls_answer.append(row)

            if ls_answer:
                bot.send_message(
                    chat_id, f"Вы уверены что хотите удалить заявку номер {number}?"
                )
                ls_send = [
                    "id",
                    "номер заявки",
                    "логин",
                    "проблема",
                    "статус",
                    "оценка",
                ]
                send_answer = ""
                for row in ls_answer:
                    for i in range(len(ls_send)):
                        send_answer += f"{ls_send[i]}: {row[i]}\n"
                bot.send_message(chat_id, send_answer)
                bot.send_message(chat_id, "да\\нет")

                bot.register_next_step_handler(message, delete_or_not)
            else:
                bot.send_message(
                    chat_id,
                    "Такой заявки нет в базе данных, убедитесь в правильности номера заявки",
                )

        def delete_or_not(message):
            nonlocal number, objects
            chat_id = message.chat.id
            if str(message.text).lower() == "нет":
                bot.send_message(chat_id, "Удаление отменено")
            elif str(message.text).lower() == "да":
                objects.del_application(number)
                bot.send_message(
                    chat_id, f"Заявка номер {number}, успешно удалина из базы данных"
                )
            else:
                bot.send_message(
                    chat_id,
                    "Не совсем вас понял\nПожалуйста введите да - если вы хотите удалить заявку\nнет - если не хотите",
                )
                bot.register_next_step_handler(message, delete_or_not)

        start_delete(message)

    wellcome(message)

    @bot.message_handler(
        func=lambda message: message.text
        in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    )
    def send_answer(message):
        global user_id, user_buttons
        grade = int(message.text)

        keyboard = telebot.types.ReplyKeyboardMarkup()

        for button in user_buttons:
            button_save = telebot.types.InlineKeyboardButton(text=button)
            keyboard.add(button_save)
        if grade > 6:
            bot.send_message(user_id, "Спасибо за вашу оценку", reply_markup=keyboard)
        else:
            bot.send_message(
                user_id,
                "Спасибо за честную оценку, мы постораемся улучшить наше обслуживание",
                reply_markup=keyboard,
            )
        objects = Applications()
        user_id = objects.get_user_id(old_number)
        objects.set_grade(old_number, grade)
        bot.register_next_step_handler(message, wellcome)
