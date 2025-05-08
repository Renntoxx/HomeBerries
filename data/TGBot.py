import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Application
from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

reply_keyboard = [['Проблемы с заказом', 'О нас'],
                  ['Оставить отзыв']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

async def start(update, context):
    photo = 'https://cdn.midjourney.com/af2a054c-f406-4d25-b83e-ddda6495e1bb/0_2.png'
    await context.bot.send_photo(
        update.message.chat_id,
        photo,
        caption="Добро пожаловать в Техническую поддержку HomeBerries! Выберите с помощью кнопок ниже,"
                "что вас интересует:",
        reply_markup=markup
        )

def start_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == "__main__":
    start_bot()