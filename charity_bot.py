import itertools
import random
from typing import List
from uuid import uuid4

import psycopg2 as psycopg2
import redis
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    InlineQueryHandler, CallbackQueryHandler, Filters, \
    ConversationHandler, MessageHandler

from config import TELEGRAM_BOT_API_KEY, DB_UN, DB_PW

API_KEY = TELEGRAM_BOT_API_KEY

reedis = redis.Redis(host='172.18.0.2')

# TODO Separate 3 different bots: inliner, hypnotalker and charity_taker

# feedback about product

OWN, THEME, KBSWITCH, DONATE, TALK_W_AUTHOR, MODERATE, SAVE_PRIVACY = range(7)
ADD_P, DELETE_P, SHOW_V, NEW_P, DLT_I = range(5)

ASKED_THROUGH = False

IDK, NO, YES = range(-1, 2)
answers2human = {
    '✅  Yes': YES,
    '❌  No': NO,
    "💁🏽  I don't know": IDK
}

# TODO add donators list through cb_ctxt
# TODO add more gifs and stickers and, maybe, sounds
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
    # TODO place check for already registered, to UPDATE or restrict
    # TODO add new user to notify_list
    """"Starts the conversetion from greetings and asks about interests to be promoted"""
    # Some information push for coordinatcions or news by interest

    update.message.reply_text("Hello! 👋🏼")
    update.message.reply_text("How you wish to change the world? 🌍 \n"
                              "What does the reality need to be made of? 🌌\n"
                              "Let us improve the messaging with some recherche words! 🧘 \n"
                              "🍀 Make the machines take our bulk to "
                              "give us a possibility improve ourselves!")


def help_msg(update: Update, context: CallbackContext):
    "Usage guideness"
    update.message.reply_text("▶️Just choose from proposed to answer\n"
                              "or just inline @smart_abbot to impress with your manners. 💫"
                              "Type '/tweak' for custom phrases menu 😉")


def info(update: Update, context: CallbackContext):
    """Information about application"""
    update.message.reply_text("👯 🤖 This Bot was made to save human "
                              "wishes and lives with a politness."
                              " Made just by help of Maecenas's❤ partials.\n "
                              # "You can buy me a coffee! ☕️"
                              # "https://www.buymeacoffee.com/greettheworldK"
                              )

    update.message.reply_text("💻 Author: JKD. Made for public use."
                              "📱 You can contact\n🏄🏽‍♂ owner here: @lolyge "
                              "🦾 Bots , crawlers 🕷, automation 🎛")


def wants(update: Update, ctxt: CallbackContext):
    """serie of questions to save people attitude to
     the thread and project, 1 by 1
    Creates the dialog with user, saving his looks(dict)
    associated with user_id in database"""
    # add checks for allready known user
    # possible solution wia custom context, much more effective way
    yn_keyboard = ReplyKeyboardMarkup(yn_kb_mu, resize_keyboard=True,
                                      one_time_keyboard=True, input_field_placeholder='Be grace to yourselves...')
    update.message.reply_text("1. 👑 Do you want to own alike bot?\n",
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
    """Working up on button pressed and
     continues dialog"""
    qury = updt.callback_query
    user_wish['theme'] = qury.data
    qury.answer()

    qury.edit_message_text(text=f'That is a nice choice. '
                                f'This will be used for latter good tiding app as '
                                f'development will go further. '
                                f'Want to ask you about things. Just say \'OK\'.')
    return KBSWITCH


def want2_to_3(updt: Update, ctxt: CallbackContext):
    """Makes transition to reply from inline"""
    # criminal raccoon handshake
    updt.message.reply_sticker('CAACAgIAAxkBAAEDYmZhpUEeM46qYBlLZU1ifmG3yDOUHwACYAYAAvoLtgg_BZcxRs21uyIE')
    yn_keyboard = ReplyKeyboardMarkup(yn_kb_mu, resize_keyboard=True,
                                      one_time_keyboard=False, input_field_placeholder='Be grace to yourselves...')
    updt.message.reply_text("3. 🤑 Do you want to enrich this bot and his owner?\n", reply_markup=yn_keyboard)
    return DONATE


def want3(updt: Update, ctxt: CallbackContext):
    """ n-th from pipe of info answer-handlers
    and question throwers"""
    updt.message.reply_text("4. 💌 Do you want to "
                            "contact with creator of this bot?\n")
    user_wish['to_pay'] = answers2human[updt.message.text]
    return TALK_W_AUTHOR


def want4(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("5. ✊🏼  Do you want to direct"
                            " and learn more about our goals?\n", )
    user_wish['to_contact'] = answers2human[updt.message.text]
    return MODERATE


def wantl(updt: Update, ctxt: CallbackContext):
    updt.message.reply_text("6. 📂 Do you want your choices and interests to be stored in our database?")
    user_wish['to_direct'] = answers2human[updt.message.text]
    return SAVE_PRIVACY


# todo work on this function composition
def save_db(updt: Update, ctxt: CallbackContext):
    """Database writing answers for statistic.
    Writes data regarding user's choice"""
    updt.message.reply_text('🌈 As you wish ✨',
                            reply_markup=ReplyKeyboardRemove())

    user_id = updt.message.from_user.id
    sql_arg_lst = [user_wish['to_own'], user_wish['to_pay'],
                   user_wish['theme'], user_wish['to_contact'], user_wish['to_direct'], str(user_id)]

    conn = psycopg2.connect(database='chares',
                            user=DB_UN,
                            password=DB_PW,
                            host='192.168.0.162',
                            # host='0.0.0.0',
                            # host='127.0.0.1',
                            port='5433')
    cur = conn.cursor()

    is_known_sql = '''SELECT * FROM public.char_wants
    WHERE user_id = %s;'''
    cur.execute(is_known_sql, (str(user_id),))
    user_dt_in_db = cur.fetchone()
    if user_dt_in_db is not None:
        # TODO bug with overwritting existing user answers from user to DB
        # is it still a problem
        raw_sql = '''UPDATE public.char_wants
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
    """Which kind of payment is convenient?💴💰"""
    pass


def op_ends(update: Update, contxt: CallbackContext):
    """Thank you!🤝 Watch for news in your thread!"""
    pass


def _prefrm(plts: List[str], syms, add_qr: bool = False) -> List[str]:
    """preparing strings for messaging"""
    prf_l = map(lambda x: syms + x + " {}", plts)
    return list(prf_l)


def cstm_menu(update: Update, cntxt: CallbackContext):
    a_s_d_cust_kb_mu = [['➕ Add', '🗒 Show'], ['❌ Delete']]
    cstmz_kb = ReplyKeyboardMarkup(a_s_d_cust_kb_mu,
                                   one_time_keyboard=True, input_field_placeholder='Improving...')
    update.message.reply_text('Please, operate with customization.',
                              reply_markup=cstmz_kb)
    return SHOW_V


def _get_cstms(usr_id):
    return reedis.smembers(usr_id)


# TODO add emty checks
def show_cstms(update: Update, cntxt: CallbackContext):
    """Listing all available patterns for user"""
    chc = update.message
    cstms = _get_cstms(chc.from_user.id)
    if not cstms:
        chc.reply_text("There is nothing to show.")
        return ConversationHandler.END
    lst_t_shw = [cstm.decode('utf-8') for cstm in cstms]
    ot_t_shw = "\n& ".join(lst_t_shw)
    chc.reply_text(f'Your custom choices are: {ot_t_shw}')
    return ConversationHandler.END


def dlt_cstm(update: Update, cntxt: CallbackContext):
    # todo make checkboxes
    """releasing the space for custom phrases
    lets to delete by the key"""
    chc = update.message
    cstms = _get_cstms(chc.from_user.id)
    if not cstms:
        chc.reply_text("There is nothing to delete.")
        return ConversationHandler.END
    cstms_t_dlt_mu = []
    for cstm in cstms:
        cstm = cstm.decode('utf-8')
        cstms_t_dlt_mu.append([InlineKeyboardButton(f'🟡 {cstm}',
                                                    callback_data=f'{cstm}')])
        print(cstm)
    print(cstms_t_dlt_mu)
    chc.reply_text("🟥 Choose phrases to delete:",
                   reply_markup=InlineKeyboardMarkup(inline_keyboard=cstms_t_dlt_mu))
    return DLT_I


def rm_frm_rds(updt: Update, cntxt: CallbackContext):
    updt_cb_q = updt.callback_query
    p2r = updt_cb_q.data
    if p2r is not None:
        reedis.srem(updt_cb_q.from_user.id, p2r)
    updt_cb_q.answer("The space is free now =)")
    return ConversationHandler.END


def ask_f_cstms(update: Update, cntxt: CallbackContext):
    """adds some custom phrases for user or group of users"""
    update.message.reply_text('Please, enter your brand expression:')
    return ADD_P


def add_t_cstms(update: Update, cntxt: CallbackContext):
    """Writes the Person's exression to db"""
    incm_msg = update.message
    nw_xprsn = incm_msg.text
    if nw_xprsn.strip() == "" or nw_xprsn is None:
        incm_msg.reply_text("This phrase is empty.")
    elif len(nw_xprsn.strip()) < 10:
        incm_msg.reply_text("Your phrase seems uneffective in usage")
    else:
        cr_usr_id = incm_msg.from_user.id
        if reedis.scard(cr_usr_id) > 10:
            reedis.spop(cr_usr_id)
            incm_msg.reply_text("Something removed...")
        reedis.sadd(cr_usr_id, nw_xprsn)
        incm_msg.reply_text("Your new tricky words are availaible now!")
    return ConversationHandler.END


def inline_pray(update: Update, context: CallbackContext):
    # TODO insert names into text dynamicly, possibly, with reply to
    # TODO switching modes (business, friendly, sarcasm, etc.)
    """Create some texts which made from affirmations, auto-training and self-hypnosis"""
    # text preview not implemented in this api
    # inl_qur = update.inline_query.query

    query = update.inline_query.query
    polite_pls = ["Be so kind ", "Please excuse me ", "Would you be so kind ",
                  "Could you please ", "We would appreciate it if you would "]
    polite_thx = ["Thank you so much for everything.", "Thank you very much for your support.",
                  "Thank you, that was very kind of you. ", "I sincerely thank you.",
                  "I wouldn't have made it without you."]
    polite_apl = ["Dear sir ", "Dear Gentleman ", "Dear Citizen "]
    polite_greeting = ["I wish you a good day!", "Incredibly glad to see you!",
                       "Greetings from the bottom of my heart!", "Hello, thanks for the contact!", ]
    polite_goodbuys = ["Hope we meet again soon.", "I was very happy to meet you!",
                       "I would like our communication to remain as warm"]
    # polite_cstms = context.user_data.get('cstm', [])

    polite_greeting = _prefrm(polite_greeting, " 👋🏼 ")
    polite_apl = _prefrm(polite_apl, " 👉🏽 👇🏾 👈🏻 ", True)
    polite_pls = _prefrm(polite_pls, "🙏🏼 🥺 ", True)
    polite_thx = _prefrm(polite_thx, "☺️")
    polite_goodbuys = _prefrm(polite_goodbuys, " 👋🏼 🕺🏽 ")

    # customs are additional feature
    cstms = reedis.smembers(update.inline_query.from_user.id)
    cstms = [cstm.decode('utf-8') for cstm in cstms]
    all_p = [polite_greeting + polite_apl + polite_pls + polite_thx + polite_goodbuys + cstms]
    all_p_sl = itertools.chain.from_iterable(all_p)
    # results will be made of matches, then just popular or genral
    # results = [], then .append for each func call it will return new result
    results_on_empt = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Eloquent good buys",
            input_message_content=InputTextMessageContent(random.choice(polite_goodbuys).format(query))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Please <your text>",
            input_message_content=InputTextMessageContent(random.choice(polite_pls).format(query))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Eloquent gratitude",
            # input_message_content=InputTextMessageContent(
            #     f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            # ),
            input_message_content=InputTextMessageContent(random.choice(polite_thx).format(query))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Address, <your text>",
            input_message_content=InputTextMessageContent(random.choice(polite_apl).format(query))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Eloquent greetings",
            input_message_content=InputTextMessageContent(random.choice(polite_greeting).format(query))
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bot chat. Feedback, set and involve.",
            input_message_content=InputTextMessageContent("💬 Bot chat appears here: @smart_abbot")
        ),
    ]

    def fnd(qr: query) -> List[str]:
        """looking for  in patterns"""
        mtchs = []
        for phrs in all_p_sl:
            if qr in phrs:
                mtchs.append(phrs)
        return mtchs

    results = [InlineQueryResultArticle(id=str(uuid4()), title=fl_phrs,
                                        input_message_content=InputTextMessageContent(fl_phrs.format(query)))
               for fl_phrs in fnd(query)]

    if query == "" or results == []:
        update.inline_query.answer(results_on_empt)
    else:
        update.inline_query.answer(results)


# TODO need to add customization, person-styled scripts

def main():
    """Dirty machinery"""
    updater = Updater(API_KEY)

    disp = updater.dispatcher

    # cbd_fltr = Filters.regex("^(Cyberspace|Friendship|Sound|Competitive|Reading|Gastronomy|Gaming)$")
    cbd_fltr = "^(Cyberspace|Friendship|Sound|Competitive|Reading|Gastronomy|Gaming)$"
    yn_filter = Filters.regex("^(✅  Yes|❌  No|💁🏽  I don't know)$")
    # thm_filter = Filters.regex("^(🎰 🎯 Gaming 🎭 🎲 |📡Cyberspace🪙|🎸🎧Sound🎼🎷|"
    #                            "🤼Competitive⛷|📖Reading📚|🥕Gastronomy🫑)$")

    # Todo customize
    cstmztn = ConversationHandler(
        entry_points=[CommandHandler('tweak', cstm_menu)],
        states={
            SHOW_V: [
                MessageHandler(Filters.regex("^➕ Add$"), ask_f_cstms),
                MessageHandler(Filters.regex("^🗒 Show$"), show_cstms),
                MessageHandler(Filters.regex("^❌ Delete$"), dlt_cstm),
            ],
            DLT_I: [CallbackQueryHandler(rm_frm_rds)],
            ADD_P: [MessageHandler(Filters.text, add_t_cstms)],
        },
        fallbacks=[]
    )
    yn_questnry = ConversationHandler(
        entry_points=[CommandHandler('wants', wants)],
        states={
            OWN: [MessageHandler(yn_filter, want1)],
            THEME: [CallbackQueryHandler(want2, pattern=cbd_fltr)],
            KBSWITCH: [MessageHandler(Filters.text, want2_to_3)],
            DONATE: [MessageHandler(yn_filter, want3)],
            TALK_W_AUTHOR: [MessageHandler(yn_filter, want4)],
            MODERATE: [MessageHandler(yn_filter, wantl)],
            SAVE_PRIVACY: [MessageHandler(yn_filter, save_db)],
        },
        fallbacks=[],
        allow_reentry=True,
    )

    # bug on update error
    disp.add_handler(cstmztn)
    disp.add_handler(CommandHandler("help", help_msg))
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
