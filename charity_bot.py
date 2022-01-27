import logging
import random
from uuid import uuid4

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackContext, InlineQueryHandler
from telegram.utils.helpers import escape_markdown

API_KEY = "2132128213:AAFWw2QEvv_RU2UWyvUYygs2MrcG85ehi8Q"

# CREDO, PAYMENT,

# feedback about product

OWN, DONATE, TALK_W_AUTHOR, MODERATE = range(4)

IDK, NO, YES = range(-1, 2)

user_wish = {
    'to_own': IDK,
    'to_pay': IDK,
    'to_contact': IDK,
    'to_direct': IDK
}


def start(update: Update, context: CallbackContext):
    """"Starts the conversetion from greetings and asks about interests to be promoted"""
    # Some information push for coordinatcions or news by interest

    reply_kb = [['Cyberspace🪙', 'Friendship👭', '🎸🎧Sound🎼🎷', 'Competitive🤼⛷', 'Reading📚',
                 'Gastronomy🥕🫑', '🎰🎯Gaming🎭🎲']]

    update.message.reply_text("Hello! 👋🏼 🧘 \
        🍀 How you wish to change the world?\
        🌍 What does the Earth need?",
                              reply_markup=ReplyKeyboardMarkup(reply_kb, one_time_keyboard=True,
                                                               input_field_placeholder="The greatest thing in human's life"))


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Just choose from proposed and make a donation💴💰.\
    You can contact owner here: @lolyge")


def info(update: Update, context: CallbackContext):
    update.message.reply_text("👯 🤖 This Bot was made to save human wishes and lives with a \
                              help of Maecenas's❤ partials. 💻 Author: JKD. Made for public use.")


def want(update: Update, ctxt: CallbackContext):
    """Creates the dialog with user, saving his looks(dict) associated with user_id in database"""
    yn_keyboard = ReplyKeyboardMarkup([['✅Yes', '❌No'], ["💁🏽I don't know"]], resize_keyboard=True,
                                      one_time_keyboard=False, input_field_placeholder='Be grace to yourselves...')
    update.message.reply_text("1. 👑 Do you wan't to own alike bot?\n"
                              "2. 🤑 Do you wan't to enrich this bot and his owner?\n"
                              "3. 💌 Do you wan't to contact with creator of this bot?\n"
                              "4. ✊🏼  Do you wan't to direct and learn more about our goals?\n",
                              reply_markup=yn_keyboard)


def recieve_money():
    "Which kind of payment is convenient?💴💰"
    pass


def op_ends(update: Update, contxt: CallbackContext):
    update.message.reply_sticker('CAACAgIAAxkBAAEDYmZhpUEeM46qYBlLZU1ifmG3yDOUHwACYAYAAvoLtgg_BZcxRs21uyIE')
    "Thank you!🤝 Watch for news in your thread!"
    pass


def inline_pray(update: Update, context: CallbackContext):
    #TODO insert names into text dynamicly
    #TODO switching modes (business, friendly, sarcasm, etc.)
    """Create some texts which made from affirmations, auto-training and self-hypnosis"""
    # inl_qur = update.inline_query.query

    query = update.inline_query.query

    if query == "":
        return
    polite_pls = ["Будьте так любезны", "Прошу вас извинить меня", "Не будете ли вы настолько добры",
                  "Не могли бы вы, пожалуйста"]
    polite_thx = ["Огромное вам спасибо за всё", "Большое вам спасибо за поддержку",
                  "Спасибо, это было очень любезно c вашей стороны", "Очень благодарен вам",
                  "Без вас я бы низачто не справился"]
    polite_apl = ["Уважаемый господин", "Молодой человек", "Дорогой гражданин"]
    polite_greeting = ["Желаю вам доброго дня!", "Невыразимо рад вас видеть!",
                       "Привествую от всего сердца!", "Здравствуйте, спасибо за коннект!", ]
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Пожалуйста",
            # input_message_content=InputTextMessageContent(query.upper()),
            input_message_content=InputTextMessageContent("🙏🏼 🥺" + random.choice(polite_pls))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Благодарность",
            # input_message_content=InputTextMessageContent(
            #     f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            # ),
            input_message_content=InputTextMessageContent( "☺️" + random.choice(polite_thx))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Обращение",
            # input_message_content=InputTextMessageContent(
            #     f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            # ),
            input_message_content=InputTextMessageContent(" 👉🏽 👇🏾 👈🏻 " + random.choice(polite_apl))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Приветствие",
            # input_message_content=InputTextMessageContent(
            #     f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            # ),
            # input_message_content=InputTextMessageContent(random.choice(polite_apl))
            input_message_content=InputTextMessageContent(" 👋🏼 " + random.choice(polite_greeting))
        )
    ]

    update.inline_query.answer(results)


#
# def inline_font(update: Update, context: CallbackContext):
#     query = update.inline_query.query
#     if query == "":
#         return
#     results = [
#         InlineQ
#     ]


def main():
    updater = Updater(API_KEY)

    disp = updater.dispatcher

    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler('info', info))
    disp.add_handler(CommandHandler('op_ends', op_ends))
    disp.add_handler(InlineQueryHandler(inline_pray))

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #     states=
    # )
    # usage_conv_hndlr = ConversationHandler(
    #     entry_points=[CommandHandler('want', want)]
    # )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
