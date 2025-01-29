import logging
import requests
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

# токен бота (имя пользователя в тг @ChecksIMEIbot)
TELEGRAM_BOT_TOKEN = "7776794505:AAGiXHAa_Q1-1GnejsitJVl0-v30KRiDQVo"


# Токен API Sandbox
API_TOKEN = "e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b"


# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Список разрешенных пользователей (белый список)
WHITELIST = ["5276576528"]  # Замените на реальные ID пользователей


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Отправь мне IMEI, и я проверю его.")


def check_imei(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)

    if user_id not in WHITELIST:
        update.message.reply_text("У вас нет доступа к этому боту.")
        return

    imei = update.message.text.strip()

    # Проверка на валидность IMEI (должен быть 15 цифр)
    if not imei.isdigit() or len(imei) != 15:
        update.message.reply_text(
            "Некорректный IMEI. Убедитесь, что он состоит из 15 цифр."
        )
        return

    # Запрос к API для проверки IMEI
    response = requests.post(
        "https://imeicheck.net/api/check-imei", data={"imei": imei, "token": API_TOKEN}
    )
    print(response)

    if response.status_code == 200:
        data = response.json()
        update.message.reply_text(f"Информация о IMEI: {data}")
    else:
        update.message.reply_text("Ошибка при проверке IMEI. Попробуйте позже.")


def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_imei))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
