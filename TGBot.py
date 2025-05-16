import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, Application, \
    CallbackQueryHandler
from config import BOT_TOKEN
from data import db_session
from data.reviews import Review

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


reply_keyboard = [
        [InlineKeyboardButton("Проблемы с заказом", callback_data='option1')],
        [InlineKeyboardButton("Помощь с сайтом", callback_data='option1.1')],
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
        photo_longdev = 'https://cdn.midjourney.com/adbd95a3-aa00-4578-ab87-6e79e5d8a307/0_2.png'
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
            photo_moremoney = 'https://cdn.midjourney.com/adbd95a3-aa00-4578-ab87-6e79e5d8a307/0_2.png'
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
            sendmessange_keyboard = [
                [create_return_button()]
            ]
            moremoney_markup = InlineKeyboardMarkup(sendmessange_keyboard)
            await query.message.reply_text("Напишите, пожалуйста, вашу проблему, и мы перенаправим вас "
                                           "нашему помощнику!",
                                           reply_markup=moremoney_markup)
            return




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
        photo_AlLep = '../static/images/Allep.png'
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

        photo_Medfed = '../static/images/Medfed.jpg'
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


        photo_KulGreg = '../static/images/Kulgreg.jpg'
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
    db_session.global_init("db/hb.db")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_review))
    application.run_polling()


if __name__ == "__main__":
    start_bot()