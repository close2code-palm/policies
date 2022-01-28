import random
from uuid import uuid4

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, InlineQueryHandler, CallbackQueryHandler, Filters, \
    ConversationHandler, MessageHandler

API_KEY = "2132128213:AAFWw2QEvv_RU2UWyvUYygs2MrcG85ehi8Q"

# CREDO, PAYMENT,

# feedback about product

OWN, DONATE, TALK_W_AUTHOR, MODERATE, SAVE_PRIVACY = range(5)

IDK, NO, YES = range(-1, 2)
answers2human = {
    '✅Yes': YES,
    '❌No': NO,
    "💁🏽I don't know": IDK
}

user_wish = {
    'theme': 'Reading',
    'to_own': IDK,
    'to_pay': IDK,
    'to_contact': IDK,
    'to_direct': IDK
}


def start(update: Update, context: CallbackContext):
    """"Starts the conversetion from greetings and asks about interests to be promoted"""
    # Some information push for coordinatcions or news by interest

    reply_kb = [[
        InlineKeyboardButton('📡Cyberspace🪙', callback_data='Cyberspace'),
        InlineKeyboardButton('✌🏼Friendship👭', callback_data='Friendship')],
        [InlineKeyboardButton('🎸🎧Sound🎼🎷', callback_data='Sound'),
         InlineKeyboardButton('🤼Competitive⛷', callback_data='Competitive')],
        [InlineKeyboardButton('📖Reading📚', callback_data='Reading'),
         InlineKeyboardButton('🥕Gastronomy🫑', callback_data='Gastronomy')],
        [InlineKeyboardButton('🎰 🎯 Gaming 🎭 🎲 ', callback_data='Gaming')]]

    update.message.reply_text("Hello! 👋🏼 🧘 \
        🍀 How you wish to change the world?\
        🌍 What does the reality need to be made of?",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=reply_kb))


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Just choose from proposed and make a donation💴💰."
                              "You can contact owner here: @lolyge")


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the user dict."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    user_wish['theme'] = query.data
    # Selected
    # option:
    # query.edit_message_text(text=f"{query.data}")


def info(update: Update, context: CallbackContext):
    update.message.reply_text("👯 🤖 This Bot was made to save human wishes and lives with a \
                              help of Maecenas's❤ partials. 💻 Author: JKD. Made for public use.")


def wants(update: Update, ctxt: CallbackContext):
    # add checks for allready known user
    # possible solution wia custom context, much more effective way
    """serie of questions to save people attitude to the thread and project, 1 by 1
    Creates the dialog with user, saving his looks(dict) associated with user_id in database"""
    yn_keyboard = ReplyKeyboardMarkup([['✅Yes', '❌No'], ["💁🏽I don't know"]], resize_keyboard=True,
                                      one_time_keyboard=False, input_field_placeholder='Be grace to yourselves...')
    update.message.reply_text("1. 👑 Do you wan't to own alike bot?\n",
                              reply_markup=yn_keyboard)
    return OWN


def want2(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("2. 🤑 Do you wan't to enrich this bot and his owner?\n")
    user_wish['to_own'] = answers2human[updt.message.text]
    return DONATE


def want3(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("3. 💌 Do you wan't to contact with creator of this bot?\n")
    user_wish['to_pay'] = answers2human[updt.message.text]
    return TALK_W_AUTHOR


def want4(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("4. ✊🏼  Do you wan't to direct and learn more about our goals?\n", )
    user_wish['to_contact'] = answers2human[updt.message.text]
    return MODERATE


def wantl(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("5. 📂 Do you wan't your choices and interests to be stored in our database?")
    user_wish['to_direct'] = answers2human[updt.message.text]
    return SAVE_PRIVACY


def save(updt: Update, ctxt: CallbackContext):
    """database writing answers for statistic"""
    updt.message.reply_text('🌈As you wish✨',
                            reply_markup=ReplyKeyboardRemove())
    pass


def recieve_money():
    "Which kind of payment is convenient?💴💰"
    pass


def op_ends(update: Update, contxt: CallbackContext):
    update.message.reply_sticker('CAACAgIAAxkBAAEDYmZhpUEeM46qYBlLZU1ifmG3yDOUHwACYAYAAvoLtgg_BZcxRs21uyIE')
    "Thank you!🤝 Watch for news in your thread!"
    pass


def inline_pray(update: Update, context: CallbackContext):
    # TODO insert names into text dynamicly
    # TODO switching modes (business, friendly, sarcasm, etc.)
    """Create some texts which made from affirmations, auto-training and self-hypnosis"""
    # TODO make responsible for requested phrase, send via preview
    # inl_qur = update.inline_query.query

    query = update.inline_query.query
    # if query == "":
    #     return

    polite_pls = ["Будьте так любезны", "Прошу вас извинить меня", "Не будете ли вы настолько добры",
                  "Не могли бы вы, пожалуйста"]
    polite_thx = ["Огромное вам спасибо за всё ", "Большое вам спасибо за поддержку ",
                  "Спасибо, это было очень любезно c вашей стороны ", "Очень благодарен вам ",
                  "Без вас я бы низачто не справился "]
    polite_apl = ["Уважаемый господин", "Молодой человек", "Дорогой гражданин"]
    polite_greeting = ["Желаю вам доброго дня!", "Невыразимо рад вас видеть!",
                       "Привествую от всего сердца!", "Здравствуйте, спасибо за коннект!", ]
    # polite_goodbuys = []
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Пожалуйста",
            input_message_content=InputTextMessageContent("🙏🏼 🥺" + random.choice(polite_pls) + query)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Благодарность",
            # input_message_content=InputTextMessageContent(
            #     f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            # ),
            input_message_content=InputTextMessageContent("☺️" + random.choice(polite_thx) + query)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Обращение",
            input_message_content=InputTextMessageContent(" 👉🏽 👇🏾 👈🏻 " + random.choice(polite_apl) + query)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Приветствие",
            input_message_content=InputTextMessageContent(" 👋🏼 " + random.choice(polite_greeting) + query)
        )
    ]

    update.inline_query.answer(results)


# TODO need to add customization, person-styled scripts

def main():
    """Dirty machinery"""
    updater = Updater(API_KEY)

    disp = updater.dispatcher

    yn_filter = Filters.regex("^(✅Yes|❌No|💁🏽I don't know)$")

    yn_questnry = ConversationHandler(
        entry_points=[CommandHandler('wants', wants)],
        states={
            OWN: [MessageHandler(yn_filter, want2)],
            DONATE: [MessageHandler(yn_filter, want3)],
            TALK_W_AUTHOR: [MessageHandler(yn_filter, want4)],
            MODERATE: [MessageHandler(yn_filter, wantl)],
            SAVE_PRIVACY: [MessageHandler(yn_filter, save)],
        },
        fallbacks=[]
    )

    # bug on update error
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler('info', info))
    disp.add_handler(CommandHandler('op_ends', op_ends))
    disp.add_handler(CallbackQueryHandler(button))
    disp.add_handler(yn_questnry)
    disp.add_handler(InlineQueryHandler(inline_pray))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
