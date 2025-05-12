import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Application, \
    CallbackQueryHandler
from config import BOT_TOKEN
from data import db_session
import os
from data.reviews import Review

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


reply_keyboard = [
        [InlineKeyboardButton("Проблемы с заказом", callback_data='option1')],
        [InlineKeyboardButton("О нас", callback_data='option2')],
        [InlineKeyboardButton("Оставить отзыв", callback_data='option3')]
    ]
markup = InlineKeyboardMarkup(reply_keyboard)

def create_return_button():
    return InlineKeyboardButton("Вернуться", callback_data='return')

async def start(update, context):
    await show_main_menu(update, context)

async def button(update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'option2':
        aboutus_keyboard = [
            [InlineKeyboardButton('О разработчиках', callback_data='aboutus')],
            [create_return_button()]
             ]
        aboutus_markup = InlineKeyboardMarkup(aboutus_keyboard)
        photo_aboutus = 'https://cdn.midjourney.com/adbd95a3-aa00-4578-ab87-6e79e5d8a307/0_2.png'
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_aboutus,
            caption=(
                "<b> 🐌 HomeBerries</b> - это интернет-магазин, вдохновленный российским интернет-магазином <i>WildBerries</i>.\n\n"
                "🛒 Мы предлагаем широкий ассортимент товаров для дома, включая <i>одежду, "
                "электронику, товары для кухни и многое другое</i>."
                "\n\n<b>✅ Наша цель</b> — сделать покупки удобными и доступными <i>для каждого клиента</i>, "
                "предоставляя качественные товары и отличный сервис.\n\n"
                "💟 HomeBerries объединяет <i>удобный интерфейс, "
                "быстрая доставка и разнообразие товаров</i>, чтобы удовлетворить потребности каждого покупателя."
            ),
            parse_mode='HTML',  # Указываем, что используем HTML
            reply_markup=aboutus_markup
        )

    if query.data == 'option3':
        feedback_keyboard = [
            [InlineKeyboardButton('Посмотреть отзывы', callback_data='show_reviews')],
            [create_return_button()]
        ]
        feedback_markup = InlineKeyboardMarkup(feedback_keyboard)
        await query.message.reply_text("Пожалуйста, напишите ваш отзыв:",
                                       reply_markup=feedback_markup)
        return  # Ожидаем текст от пользователя

    if query.data == 'show_reviews':
        await show_reviews(update.callback_query, context)

    if query.data == 'return':
        await show_main_menu(update.callback_query, context)

async def show_main_menu(update, context):
    photo = 'https://cdn.midjourney.com/af2a054c-f406-4d25-b83e-ddda6495e1bb/0_2.png'
    await context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=photo,
        caption="Добро пожаловать в Техническую поддержку HomeBerries! Выберите с помощью кнопок ниже, "
                "что вас интересует:",
        reply_markup=markup
        )

async def show_reviews(update, context):
    db_sess = db_session.create_session()
    reviews = db_sess.query(Review).all()

    if reviews:
        reviews_text = "\n".join([f"Отзыв '{review.id}: {review.review}', {review.created_at[:10]}" for review in reviews])
        await update.message.reply_text(reviews_text)
    else:
        await update.message.reply_text("Отзывов пока нет.")

async def handle_review(update, context):
    user_id = update.message.from_user.id
    review_text = update.message.text

    # Сохраняем отзыв в базе данных
    db_sess = db_session.create_session()
    review = Review(user_id=user_id, review=review_text)
    db_sess.add(review)
    db_sess.commit()

    await update.message.reply_text("Ваш отзыв успешно отправлен!")


def start_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    db_session.global_init("../db/hb.db")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_review))
    application.run_polling()


if __name__ == "__main__":
    start_bot()