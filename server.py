import config
import sys
import telegram.bot
import logging
from mqwrapper import MQBot
from telegram.ext import messagequeue as mq
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext, ConversationHandler
from telegram import Update, User, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.utils.request import Request
import user
from datetime import datetime
from utils import serialize_datetime

# SEX, AGE, WEIGHT, HEIGHT = range(4)
SEX = range(1)

formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatstr)
logging.basicConfig(format=formatstr,level=logging.INFO)

logger = logging.getLogger(__name__)
filehandler = logging.FileHandler('log.log')
filehandler.setLevel(logging.INFO)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)


def start(update: Update, context: CallbackContext):
    msg = '''
        Добро пожаловать в естьбот!
        Это бот, который поможет вам контроллировать ваше питание
        Для инициализации вашей программы питания нужнно ввести ваши начальные показатели
    '''

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    user.add_user(update.effective_user['id'], serialize_datetime(datetime.today()))
    print(update.effective_user)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите ваш возраст: ')

def start(update, context):
    reply_keyboard = [['Men', 'Women']]
    update.message.reply_text(
        'Добро пожаловать в естьбот!'
        'Это бот, который поможет вам контроллировать ваше питание'
        'Для инициализации вашей программы питания нужнно ввести ваши начальные показатели'
        'Введите ваш пол: ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SEX

def sex(update, context):
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('На этом настройка бота завершена, приятного пользования!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

if __name__ == '__main__':
    # for test purposes limit global throughput to 3 messages per 3 seconds
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    # set connection pool size for bot
    request = Request(con_pool_size=8,
                      proxy_url=config.REQUEST_KWARGS['proxy_url'],
                      urllib3_proxy_kwargs=config.REQUEST_KWARGS['urllib3_proxy_kwargs'])
    mqbot = MQBot(config.TOKEN, request=request, mqueue=q)
    upd = telegram.ext.updater.Updater(bot=mqbot, use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            SEX: [MessageHandler(Filters.regex('^(Men|Women)$'), sex)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    upd.dispatcher.add_handler(conv_handler)

    upd.start_polling()