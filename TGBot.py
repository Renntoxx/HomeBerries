import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, Application, \
    CallbackQueryHandler
from config import BOT_TOKEN
from data import db_session
from datetime import datetime, timedelta

user_last_rating_time = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

user_requests = {}
ADMIN_ID = 713056261
reply_keyboard = [
        [InlineKeyboardButton("Проблемы с заказом", callback_data='option1')],
        [InlineKeyboardButton("Помощь с сайтом", callback_data='option1.1')],
        [InlineKeyboardButton("О нас", callback_data='option2')],
        [InlineKeyboardButton('Оставить отзыв', callback_data='feedback')]
    ]
markup = InlineKeyboardMarkup(reply_keyboard)

def create_return_button():
    return InlineKeyboardButton("Вернуться", callback_data='return')

async def start(update, context):
    await show_main_menu(update, context)

async def button(update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'option1':
        problem_keyboard = [
            [InlineKeyboardButton('Долгая доставка', callback_data='longdeliv')],
            [InlineKeyboardButton('Проблема с пополнением баланса', callback_data='moremoney')],
            [InlineKeyboardButton('Написать в техподдержку', callback_data='sendmessange')],
            [create_return_button()]
        ]
        problem_markup = InlineKeyboardMarkup(problem_keyboard)
        photo_problem = 'https://cdn.midjourney.com/adbd95a3-aa00-4578-ab87-6e79e5d8a307/0_2.png'
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_problem,
            caption=(
                " 🐌 В HomeBerries мы понимаем, что проблемы с заказами могут возникать в любой момент,"
                " и именно для этого была создана служба технической поддержки. \n\n"
                "❗ Наша команда готова помочь вам с любыми вопросами, связанными с пополнением баланса и "
                "доставкой заказов."
                "Мы стремимся обеспечить высокий уровень обслуживания и быстрое решение любых проблем,"
                "предоставляя качественные товары и отличный сервис.\n\n"
                "💟 <b>Если остались другие вопросы, то"
                " обращайтесь в нашу техподдержку, и мы с радостью поможем вам, перенаправив на нашего помощника! </b>"
            ),
            parse_mode='HTML',  # Указываем, что используем HTML
            reply_markup=problem_markup
        )

    if query.data == 'longdeliv':
        longdev_keyboard = [
            [InlineKeyboardButton('Написать в техподдержку', callback_data='sendmessange')],
            [create_return_button()]
        ]
        photo_longdev = 'https://cdn.midjourney.com/df54fb1c-97b9-4299-aa24-a4112a7fc29d/0_0.png'
        longdev_markup = InlineKeyboardMarkup(longdev_keyboard)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_longdev,
            caption=(
                " 🐌 К сожалению, из-за большого количества заказов мы не всегда успеваем доставлять вовремя. \n\n"
                "Чаще всего задержка занимает 1-2 дня, и мы высылаем письмо на почту с задержкой заказа. \n\n"
                "💟 Если вам до сих пор не пришел заказ или остались вопросы, мы всегда поможем вам в техподдержке!"
            ),
            parse_mode='HTML',  # Указываем, что используем HTML
            reply_markup=longdev_markup
        )

    if query.data == 'moremoney':
        moremoney_keyboard = [
            [InlineKeyboardButton('Написать в техподдержку', callback_data='sendmessange')],
            [create_return_button()]
        ]
        photo_moremoney = 'https://cdn.midjourney.com/4abbd7e5-fbac-4f99-9048-462cd56dc792/0_0.png'
        moremoney_markup = InlineKeyboardMarkup(moremoney_keyboard)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_moremoney,
            caption=(
                " 🐌 Чаще всего решение проблемы заключается в том, что надо обновить сайт, и тогда деньги"
                " будут зачислены. \n\n"
                "💟 Но если вам это не помогло, то техподдержка всегда сможет вам помочь!"
            ),
            parse_mode='HTML',  # Указываем, что используем HTML
            reply_markup=moremoney_markup
        )

    if query.data == 'sendmessange':
        await query.message.reply_text(text="Добро пожаловать! Напишите свой вопрос, и мы ответим вам.")
        return

    if query.data == 'option1.1':
        aboutus_keyboard = [
            [InlineKeyboardButton('Создать аккаунт', callback_data='aboutus')],
            [InlineKeyboardButton('Войти в аккаунт', callback_data='aboutus')],
            [InlineKeyboardButton('Выложить свой товар', callback_data='aboutus')],
            [InlineKeyboardButton('Пополнение баланса', callback_data='aboutus')],
            [InlineKeyboardButton('Как найти нужный товар?', callback_data='aboutus')],
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

    if query.data == 'aboutus':
        photo_AlLep = 'static/images/Allep.png'
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_AlLep,
            caption=(
                "<b>🐌 Александр Лепихов</b> - фронтенд-разработчик, который сыграл ключевую роль в визуализации "
                "нашего сайта. \n\n"
                "Им реализован интуитивно понятный и привлекательный интерфейс,"
                " который обеспечивает пользователям удобный доступ к широкому ассортименту товаров. \n\n"
                "Его креативный подход и внимание к деталям сделали HomeBerries не"
                " <i>только функциональным, но и эстетически привлекательным ресурсом для покупателей</i>."
            ),

            parse_mode='HTML'
        )

        photo_Medfed = 'static/images/Medfed.png'
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_Medfed,
            caption=(
            "<b> 🐌 Федор Мединский</b> - бэкэнд-разработчик, который отвечает за создание основного"
            " кода на Python для сайта HomeBerries. \n\n"
            "Им реализована серверная часть и работа с базами данных, которые позволяют обеспечивать "
            "<i>высокую производительность и надежность платформы.</i> \n\n"
            "Федор разрабатывает API и интеграции, которые обеспечивают бесперебойное взаимодействие между фронтендом "
            "и бэкэндом, а также реализует функционал, который делает покупки удобными и"
            " безопасными для пользователей."
            ),
            parse_mode='HTML'
        )


        return_keyboard = [
            [create_return_button()]
        ]
        return_markup = InlineKeyboardMarkup(return_keyboard)


        photo_KulGreg = 'static/images/KulGreg.png'
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_KulGreg,
            caption=(
                "<b> 🐌 Григорий Кулаков </b> -  разработчик, создавший бота технической поддержки"
                " в Telegram для сайта HomeBerries. \n\n"
                "Его работа включает в себя <i>разработку функционала, который позволяет пользователям "
                "быстро получать ответы на вопросы и решать проблемы</i>, связанные с покупками, а также подробнее"
                "узнать о разработчиках и оставить свой отзыв.\n\n"
                "Поэтому пользователи HomeBerries могут легко и эффективно получать необходимую помощь, что "
                "значительно улучшает качество обслуживания и повышает удовлетворенность клиентов. "
            ),
            parse_mode='HTML',
            reply_markup=return_markup
        )

    if query.data == 'feedback':
        query.answer()
        feedback_keyboard = [
            [InlineKeyboardButton("1", callback_data='rating_1')],
            [InlineKeyboardButton("2", callback_data='rating_2')],
            [InlineKeyboardButton("3", callback_data='rating_3')],
            [InlineKeyboardButton("4", callback_data='rating_4')],
            [InlineKeyboardButton("5", callback_data='rating_5')]
        ]
        feedback_markup = InlineKeyboardMarkup(feedback_keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Ваш отзыв очень важен для нас, ведь нам понять, нравится ли вам наш сервис или нет."
                 f"Пожалуйста, оцените нас сервис с помощью цифр выше. \n\n"
                 f"Если вас не устраивает конкретный вопрос - мы всегда рады его услышать в техподдержке!",
            reply_markup=feedback_markup
        )


    if query.data == 'one' or query.data == 'two' or query.data == 'three' or query.data == 'four' or query.data == 'five':
        user_id = query.from_user.id
        current_time = datetime.now()
        if user_id in user_last_rating_time:
            last_rating_time = user_last_rating_time[user_id]
            if current_time < last_rating_time + timedelta(hours=1):
                await query.message.reply_text("Вы уже оставили оценку. Пожалуйста, подождите 1 час.")
            else:
                await query.message.reply_text(f"Спасибо за вашу оценку!")

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


async def handle_message(update, context):

    user_id = update.message.from_user.id

    user_question = update.message.text


    # Сохраняем вопрос в глобальной переменной
    user_requests[user_id] = user_question

    # Уведомляем администратора о новом вопросе
    admin_chat_id = '713056261'  # Замените на ID чата администратора
    await context.bot.send_message(
        chat_id=admin_chat_id,
        text=f"Новый вопрос от пользователя {user_id}: {user_question}\n\nОтветьте на него."
    )

    await update.message.reply_text("Ваш вопрос успешно отправлен! Ожидайте ответа.")
    return await handle_response(update, context)

async def handle_response(update, context: CallbackContext):
    response_text = update.message.text
    admin_id = update.message.from_user.id  # Получаем ID администратора

    # Проверяем, является ли отправитель администратором
    if admin_id == 713056261:  # Замените на ID вашего администратора
        # Отправляем ответ всем пользователям, которые задали вопросы
        for user_id in user_requests.keys():
            await context.bot.send_message(
                chat_id=user_id,
                text=f"Приветствую, я - ваш помощник HomeBerries. {response_text}. Хорошего дня"
                     f" и приятных покупок!"  # Указываем, что ответ от администратора
            )
        user_requests.clear()  # Очищаем сохраненные запросы


def start_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    db_session.global_init("db/hb.db")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    application.run_polling()


if __name__ == "__main__":
    start_bot()