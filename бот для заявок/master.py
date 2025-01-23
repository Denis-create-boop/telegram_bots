from admin import *
from table import Applications


id_master = 5276576528


def master(message):

    @bot.message_handler(func=lambda message: str(message.text).lower() == "start")
    def wellcome(message):
        global photo
        chat_id = message.chat.id
        keyboard = telebot.types.ReplyKeyboardMarkup()

        for button in master_buttons:
            button_save = telebot.types.InlineKeyboardButton(text=button)
            keyboard.add(button_save)
        with open("images/avatar_main.jpg", "rb") as photo:
            bot.send_media_group(chat_id, [InputMediaPhoto(photo)])
        bot.send_message(
            chat_id,
            "Добро пожаловать в бот ДВП Воронеж ЦО",
            reply_markup=keyboard
        )

    wellcome(message)

    # меню мастера
    @bot.message_handler(func=lambda message: message.text in master_handlers)
    def master_control(message):
        def main_control(message):
            chat_id = message.chat.id
            text = message.text
            if text == "Заявку выполнил":
                bot.send_message(chat_id, "Введите номер выполненной заявки")
                bot.register_next_step_handler(message, checking_status)

            elif text == "start":
                bot.register_next_step_handler(message, wellcome)

            elif text == "Невозможно решить проблему":
                bot.send_message(chat_id, "Введите номер заявки")
                bot.register_next_step_handler(message, unpossible)
            else:
                bot.send_message(chat_id, "Хорошо, спасибо за работу")

        def unpossible(message):
            chat_id = message.chat.id
            try:
                NUM = int(message.text)
                objects = Applications()
                objects.set_new_status(NUM, "Невозможно решить проблему")
                bot.send_message(chat_id, "Хорошо, спасибо я передам")
            except:
                return message.text

        def checking_status(message):
            global user_id, master_buttons

            objects = Applications()
            chat_id = message.chat.id
            try:
                NUM = int(message.text)
                user_id = int(objects.get_user_id(NUM))
                check = objects.get_status(NUM)
                if check[0] != "Выполнена":
                    user_id = objects.get_user_id(NUM)
                    grade_keyboard = telebot.types.ReplyKeyboardMarkup()
                    grade_buttons = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
                    for button in grade_buttons:
                        button_save = telebot.types.InlineKeyboardButton(text=button)
                        grade_keyboard.add(button_save)

                    bot.send_message(chat_id, "Хорошо, спасибо за работу!")
                    bot.send_message(
                        user_id,
                        f"Ваша заявка под номером {NUM} - Выполнена\nПожалуйста оцените качество работы от 1 до 10",
                        reply_markup=grade_keyboard,
                    )
                    # keyboard = telebot.types.ReplyKeyboardMarkup()
                    #
                    # for button in master_buttons:
                    #    button_save = telebot.types.InlineKeyboardButton(text=button)
                    #    keyboard.add(button_save)
                    #
                    # bot.send_message(
                    #    chat_id,
                    #    f"Добро пожаловать в бот ДВП Воронеж ЦО",
                    #    reply_markup=keyboard,
                    # )
                    objects.set_new_status(NUM, "Выполнена")
                    bot.register_next_step_handler(message, wellcome)
                else:
                    bot.send_message(chat_id, "Хорошо, спасибо")
            except:
                return message.text

        main_control(message)

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
