import random
from uuid import uuid4

import psycopg2 as psycopg2
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, InlineQueryHandler, CallbackQueryHandler, Filters, \
    ConversationHandler, MessageHandler

API_KEY = "2132128213:AAFWw2QEvv_RU2UWyvUYygs2MrcG85ehi8Q"

# CREDO, PAYMENT,

# feedback about product

# TODO take away markups
OWN, THEME,KBSWITCH, DONATE, TALK_W_AUTHOR, MODERATE, SAVE_PRIVACY = range(7)

ASKED_THROUGH = False

IDK, NO, YES = range(-1, 2)
answers2human = {
    '✅  Yes': YES,
    '❌  No': NO,
    "💁🏽  I don't know": IDK
}

user_wish = {
    'theme': 'Reading',
    'to_own': IDK,
    'to_pay': IDK,
    'to_contact': IDK,
    'to_direct': IDK,
    # 'asked': False
}

yn_kb_mu = [['✅  Yes', '❌  No'], ["💁🏽  I don't know"]]


def start(update: Update, context: CallbackContext):
    # TODO make interface more guided through usability, not flashing from start
    # TODO place check for allready registerred, to UPDATE or restrict
    """"Starts the conversetion from greetings and asks about interests to be promoted"""
    # Some information push for coordinatcions or news by interest

    update.message.reply_text("Hello! 👋🏼"
                              "How you wish to change the world? 🌍 "
                              "What does the reality need to be made of? 🌌"
                              "Let us improve the messaging with some recherche words! 🧘 "
                              "🍀 Make the machines take our bulk to give us a possibility improve ourselves!")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("▶️Just choose from proposed to answer\n"
                              "or just inline to impress. 💫")


#  totaly forgoten functionality
# <SAFE DELETE THIS>
# GET WHAT IT IS IF POSSIBLE
# def button(update: Update, context: CallbackContext) -> None:
#     """Parses the CallbackQuery and updates the user dict."""
#     query = update.callback_query
#
#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()
#     user_wish['theme'] = query.data
#     # Selected
#     # option:
#     # query.edit_message_text(text=f"{query.data}")


def info(update: Update, context: CallbackContext):
    """Information about application"""
    update.message.reply_text("👯 🤖 This Bot was made to save human wishes and lives with a politness."
                              " Made just by help of Maecenas's❤ partials.\n 💻 Author: JKD. Made for public use."
                              "📱 You can contact\n🏄🏽‍♂ owner here: @lolyge "
                              "🦾 Bots , crawlers 🕷, automation 🎛")


def wants(update: Update, ctxt: CallbackContext):
    # add checks for allready known user
    # possible solution wia custom context, much more effective way
    """serie of questions to save people attitude to the thread and project, 1 by 1
    Creates the dialog with user, saving his looks(dict) associated with user_id in database"""
    yn_keyboard = ReplyKeyboardMarkup(yn_kb_mu, resize_keyboard=True,
                                      one_time_keyboard=True, input_field_placeholder='Be grace to yourselves...')
    update.message.reply_text("1. 👑 Do you wan't to own alike bot?\n",
                              reply_markup=yn_keyboard)
    return OWN


def want1(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("That's it...", reply_markup=ReplyKeyboardRemove())
    user_wish['to_own'] = answers2human[updt.message.text]

    reply_kb = [[
        InlineKeyboardButton('📡Cyberspace🪙', callback_data='Cyberspace'),
        InlineKeyboardButton('✌🏼Friendship👭', callback_data='Friendship', )],
        [InlineKeyboardButton('🎸🎧Sound🎼🎷', callback_data='Sound'),
         InlineKeyboardButton('🤼Competitive⛷', callback_data='Competitive')],
        [InlineKeyboardButton('📖Reading📚', callback_data='Reading'),
         InlineKeyboardButton('🥕Gastronomy🫑', callback_data='Gastronomy')],
        [InlineKeyboardButton('🎰 🎯 Gaming 🎭 🎲 ', callback_data='Gaming')]]
    updt.message.reply_text("2. What kind of activity makes your heart beat faster?",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=reply_kb))
    return THEME


def want2(updt: Update, ctxt: CallbackContext):
    "Working up on button pressed and continues dialog"
    qury = updt.callback_query
    user_wish['theme'] = qury
    qury.answer()

    qury.edit_message_text(text=f'That is a nice choice. Want to ask you about things. Just say \'OK\'.')
    return KBSWITCH


def want2_to_3(updt: Update, ctxt: CallbackContext):
    """Makes transition to reply from inline"""
    yn_keyboard = ReplyKeyboardMarkup(yn_kb_mu, resize_keyboard=True,
                                      one_time_keyboard=False, input_field_placeholder='Be grace to yourselves...')
    updt.message.reply_text("3. 🤑 Do you wan't to enrich this bot and his owner?\n", reply_markup= yn_keyboard)
    return DONATE


def want3(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("4. 💌 Do you wan't to contact with creator of this bot?\n")
    user_wish['to_pay'] = answers2human[updt.message.text]
    return TALK_W_AUTHOR


def want4(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("5. ✊🏼  Do you wan't to direct and learn more about our goals?\n", )
    user_wish['to_contact'] = answers2human[updt.message.text]
    return MODERATE


def wantl(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("6. 📂 Do you wan't your choices and interests to be stored in our database?")
    user_wish['to_direct'] = answers2human[updt.message.text]
    return SAVE_PRIVACY


def save(updt: Update, ctxt: CallbackContext):
    """Database writing answers for statistic.
    Writes data regarding user's choice"""
    updt.message.reply_text('🌈 As you wish ✨',
                            reply_markup=ReplyKeyboardRemove())

    user_id = updt.message.from_user.id
    sql_arg_lst = [user_wish['to_own'], user_wish['to_pay'],
                   user_wish['theme'], user_wish['to_contact'], user_wish['to_direct'], str(user_id)]

    conn = psycopg2.connect(database='chares',
                            user='charecommander',
                            password='tob1',
                            host='localhost',
                            port='5433')
    cur = conn.cursor()

    is_known_sql = f'''SELECT * FROM public.char_wants
    WHERE user_id = %s;'''
    cur.execute(is_known_sql, (str(user_id),))
    user_dt_in_db = cur.fetchone()
    if user_dt_in_db is not None:
        raw_sql = f'''UPDATE public.char_wants 
        SET w_t_own = %s,
            w_t_pay = %s, 
            theme = %s,
            w_t_contact = %s,
            w_t_direct = %s
        WHERE user_id = %s;'''

        cur.execute(raw_sql, sql_arg_lst)

    else:
            raw_sql = '''INSERT INTO public.char_wants (user_id, w_t_own, w_t_pay,
        theme,w_t_contact,w_t_direct) VALUES (%s,%s,%s,%s,%s,%s);'''
            cur.execute(raw_sql, (sql_arg_lst[-1], *sql_arg_lst[:-1]))
    conn.commit()
    cur.close()
    conn.close()


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
    # text preview not implemented in this api
    # inl_qur = update.inline_query.query

    query = update.inline_query.query
    # if query == "":
    #     return
    # TODO english payloads, to make THIS BROBOT more accessible and usefull. and sure, to keep style clean
    # TODO add emojis
    polite_pls = ["Be so kind ", "Please excuse me ", "Would you be so kind ",
                  "Could you please ", "We would appreciate it if you would "]
    polite_thx = ["Thank you so much for everything.", "Thank you very much for your support.",
                  "Thank you, that was very kind of you. ", "I sincerely thank you.",
                  "I wouldn't have made it without you."]
    polite_apl = ["Dear sir, ", "Dear Gentleman, ", "Dear Citizen, "]
    polite_greeting = ["I wish you a good day!", "Incredibly glad to see you!",
                       "Greetings from the bottom of my heart!", "Hello, thanks for the contact!", ]
    polite_goodbuys = ["Hope we meet again soon.", "I was very happy to meet you!",
                       "I would like our communication to remain as warm"]
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Eloquent good buys",
            input_message_content=InputTextMessageContent(" 👋🏼 🕺🏽 " + random.choice(polite_goodbuys) + query)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Please <your text>",
            input_message_content=InputTextMessageContent("🙏🏼 🥺" + random.choice(polite_pls) + query)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Eloquent gratitude",
            # input_message_content=InputTextMessageContent(
            #     f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            # ),
            input_message_content=InputTextMessageContent("☺️" + random.choice(polite_thx) + query)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Address, <your text>",
            input_message_content=InputTextMessageContent(" 👉🏽 👇🏾 👈🏻 " + random.choice(polite_apl) + query)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Eloquent greetings",
            input_message_content=InputTextMessageContent(" 👋🏼 " + random.choice(polite_greeting) + query)
        )
    ]

    update.inline_query.answer(results)


# TODO need to add customization, person-styled scripts

def main():
    """Dirty machinery"""
    updater = Updater(API_KEY)

    disp = updater.dispatcher

    # cbd_fltr = Filters.regex("^(Cyberspace|Friendship|Sound|Competitive|Reading|Gastronomy|Gaming)$")
    cbd_fltr = "^(Cyberspace|Friendship|Sound|Competitive|Reading|Gastronomy|Gaming)$"
    yn_filter = Filters.regex("^(✅  Yes|❌  No|💁🏽  I don't know)$")
    thm_filter = Filters.regex("^(🎰 🎯 Gaming 🎭 🎲 |📡Cyberspace🪙|🎸🎧Sound🎼🎷|"
                               "🤼Competitive⛷|📖Reading📚|🥕Gastronomy🫑)$")

    yn_questnry = ConversationHandler(
        entry_points=[CommandHandler('wants', wants)],
        states={
            OWN: [MessageHandler(yn_filter, want1)],
            THEME: [CallbackQueryHandler(want2, pattern=cbd_fltr)],
            KBSWITCH: [MessageHandler(Filters.text, want2_to_3)],
            DONATE: [MessageHandler(yn_filter, want3)],
            TALK_W_AUTHOR: [MessageHandler(yn_filter, want4)],
            MODERATE: [MessageHandler(yn_filter, wantl)],
            SAVE_PRIVACY: [MessageHandler(yn_filter, save)],
        },
        fallbacks=[],
        allow_reentry=True,
    )

    # bug on update error
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler('info', info))
    # disp.add_handler(CommandHandler('op_ends', op_ends))
    # disp.add_handler(CallbackQueryHandler(want1))
    disp.add_handler(yn_questnry)
    disp.add_handler(InlineQueryHandler(inline_pray))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
