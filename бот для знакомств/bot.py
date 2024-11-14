from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


# тут будем писать наш код :)
async def start(update, context):
    dialog.mod = 'main'
    text = load_message('main')
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        'start': 'запустить',
        'profile': 'генерация Tinder-профля 😎',
        'opener': 'сообщение для знакомства 🥰',
        'message': 'переписка от вашего имени 😈',
        'date': 'переписка со звездами 🔥',
        'gpt': 'задать вопрос чату GPT 🧠'
    })


async def gpt(update, context):
    dialog.mod = 'gpt'
    text = load_message('gpt')
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt('gpt')
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


async def date(update, context):
    dialog.mod = 'date'
    text = load_message('date')
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "date_grande": "Ариана Гранде",
        "date_robbie": "Марго Робби",
        "date_zendaya": "Зендея",
        "date_gosling": "Райан Гослинг",
        "date_hardy": "Том Харди",
        "date_rianna": "Рианна",
        "date_kruz": "Том Круз"
    })


async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "набирает текст...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)



async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_text(update, context, "Отличный выбор! Пригласите девушку (парня) на свидание за 5 сообщений")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mod = "message"
    text = load_message("message")
    await send_photo(update, context, "message")
    await send_text(update, context, text)
    await send_text_buttons(update, context, text, {
        'message_next': 'Следующее сообщение',
        'message_date': 'Пригласить на свидание'
    })
    dialog.list.clear()


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "Chat gpt 🧠 думает на вариантами ответа...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def profile(update, context):
    dialog.mod = 'profile'
    text = load_message('profile')
    await send_photo(update, context, 'profile')
    await send_text(update, context, text)
    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "как вас зовут?")


async def profile_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] = text
        await send_text(update, context, "кем вы работаете?")
    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, context, "сколько вам лет?")
    elif dialog.count == 3:
        dialog.user["occupation"] = text
        await send_text(update, context, "🤡какие у вас хобби?")

    elif dialog.count == 4:
        dialog.user["hobby"] = text
        await send_text(update, context, "что вам не нравиться в людях?😡")

    elif dialog.count == 5:
        dialog.user["annoys"] = text
        await send_text(update, context, "цели знакомства❤️👀?")

    elif dialog.count == 6:
        dialog.user["goals"] = text

        prompt = load_prompt('profile')
        user_info = dialog_user_info_to_str(dialog.user)
        my_message = await send_text(update, context, "chat GPT🧠 занимаеться генерацией вашего профиля подождите...")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)


async def opener(update, context):
    dialog.mod = "opener"
    text = load_message('opener')
    await send_photo(update, context, 'opener')
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "имя девушки?")

async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] = text
        await send_text(update, context, "сколько ей лет?")

    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, context, "оцените её внешность от 1 до 10")

    elif dialog.count == 3:
        dialog.user["handsome"] = text
        await send_text(update, context, "кем она работает?")

    elif dialog.count == 4:
        dialog.user["occupation"] = text
        await send_text(update, context, "цель знакомства?")

    elif dialog.count == 5:
        dialog.user["goals"] = text

        prompt = load_prompt('opener')
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "chat GPT🧠 занимаеться генерацией вашего openera подождите...")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)



async def hello(update, context):
    if dialog.mod == 'gpt':
        await gpt_dialog(update, context)
    elif dialog.mod == 'date':
        await date_dialog(update, context)
    elif dialog.mod == 'message':
        await message_dialog(update, context)
    elif dialog.mod == 'profile':
        await profile_dialog(update, context)
    elif dialog.mod == 'opener':
        await opener_dialog(update, context)

    else:

        await send_text(update, context, '*Привет*')
        await send_text(update, context, '_как дела?, я бот помощьник)_')
        await send_text(update, context, 'выберите или напишите что хотите сделать😸')

        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "как вам моя работа?", {
            'good': 'Отлично',
            'bad': 'Всё плохо'
        })


async def hello_button(update, context):
    query = update.callback_query.data
    if query == 'good':
        await send_text(update, context, '*Спасибо большое я очень рад что вам понравилось🥰😇*')
    else:
        await send_text(update, context, '*Спасибо я учту ваше мнение😒*')


dialog = Dialog()
dialog.mod = None
dialog.list = []
dialog.count = 0
dialog.user = {}

chatgpt = ChatGptService(token="gpt:1EprHW2fyrbq2MNxmQbRJFkblB3TJuC8zKn6VeGdT0tnEKbw")

app = ApplicationBuilder().token("7451810995:AAHbfdoXLlbTSVYwi1RjxJbV5F5qVlOBmrM").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("opener", opener))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_button))


app.run_polling()
