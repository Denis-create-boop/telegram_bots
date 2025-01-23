from admin import *
from master import master, id_master


users = None

@bot.message_handler(func=lambda message: str(message.text).lower() == "start")
def wellcome(message):
    global id_user
    chat_id = message.chat.id

    if chat_id == id_admin:
        id_user = id_admin
        admin(message)

    elif chat_id == id_master:
        id_user = id_master
        master(message)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup()

        for button in user_buttons:
            button_save = telebot.types.InlineKeyboardButton(text=button)
            keyboard.add(button_save)

        bot.send_message(
            chat_id, f"Добро пожаловать в бот ДВП Воронеж ЦО", reply_markup=keyboard
        )


@bot.message_handler(func=lambda message: message.text in user_handlers)
# функция для создания вопроса
def cant_connect(message):
    global question
    question = message.text
    chat_id = message.chat.id
    if question == "🔥🔥🤯Очень срочно ничего не работает🤯🔥🔥":
        bot.send_message(
            chat_id,
            "Какой ужас 😱😱\nСейчас мы все немедленно решим🧐\n Введите свой логин",
        )
        bot.register_next_step_handler(message, save_question)
    elif (
        question == "📩Не могу зайти в почту📩"
        or question == "☁️Не могу зайти на портал☁️"
        or question == "Не работает комп🤬🤬"
    ):
        bot.send_message(chat_id, "Введите свой логин")
        bot.register_next_step_handler(message, save_question)
    elif question == "Другое":
        bot.send_message(chat_id, "Напишите что у вас произошло")
        question = message.text
        bot.register_next_step_handler(message, cant_connect)
    elif str(question).lower() == "start":
        wellcome(message)
    else:
        bot.send_message(chat_id, "Введите свой логин")
        bot.register_next_step_handler(message, save_question)


# функция для описания другой проблемы
def another(message):
    global question
    question = message.text
    bot.register_next_step_handler(message, cant_connect)


# запись заявки в базу данных и отправка мастеру
def save_question(message):
    global question, users
    if message.text == "/start" or message.text == "start":
        bot.register_next_step_handler(message, wellcome)
    else:
        chat_id = message.chat.id
        users = chat_id
        name = message.text
        objects = Table(name, question, "в ожидании", chat_id)
        number = objects.write_question()
        bot.send_message(
            chat_id,
            f"""Ваша заявка отправлена специалисту номер вашей заявки {number}\n
Вы можете следить за статусом выполнения в этом боте""",
        )
        send_master(name, number, chat_id)


# функция для отправки заявки мастеру
def send_master(name, number, id_quest):
    global question
    bot.send_message(
        id_master, f"Заявка номер {number}, от пользователя {name}\n\n{question}"
    )
    buttons = ["Заявку принял", "В работе", "Выполнена"]
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for button in buttons:
        button_save = telebot.types.InlineKeyboardButton(text=button)
        keyboard.add(button_save)
    bot.send_message(id_master, "Укажите статус заявки", reply_markup=keyboard)
    answers = {
        "ok": "Заявку принял",
        "process": "В работе",
        "got": "Выполнена",
    }

    @bot.message_handler(func=lambda message: message.text in answers.values())
    def send_answer(message):
        answer = message.text
        objects = Table()
        def menu():
            global id_master
            keyboard = telebot.types.ReplyKeyboardMarkup()
            buttons = [
                "start",
                "Заявку выполнил",
                "Передал заявку другому специалисту",
                "Невозможно решить проблему",
            ]
            for button in buttons:
                button_save = telebot.types.InlineKeyboardButton(text=button)
                keyboard.add(button_save)
            bot.send_message(
                id_master,
                "Спасибо передам",
                reply_markup=keyboard,
                )
        menu()


        if answer == "Заявку принял":
            objects.set_new_status(number, "Передана специалисту")
            bot.send_message(
                id_quest,
                "Вашу заявку приняли в работу",
            )
        elif answer == "В работе":
            objects.set_new_status(number, "В работе")
            bot.send_message(
                id_quest,
                "Ваша заявка находиться в процессе решения",
 
            )
        elif answer == "Выполнена":
            bot.send_message(
                id_quest, "Вас вопрос уже решен, извините за неудобства"
            )
    
            objects.set_new_status(number, "Выполнена")

        bot.register_next_step_handler(message, wellcome)


# Функция для просмотра статуса заявки
@bot.message_handler(
    func=lambda message: message.text == "Посмотреть статус заявки👀"
)

def get_status(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ведите номер вашей заявки")
    bot.register_next_step_handler(message, show_status)


def show_status(message):
    chat_id = message.chat.id
    status = message.text
    objects = Table()
    bot.send_message(
        chat_id, f"Статус вашей заявки - {objects.get_status(status)[0]}"
    )


if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()
