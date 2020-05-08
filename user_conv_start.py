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

logger = logging.getLogger(__name__)

SEX, AGE, WEIGHT, HEIGHT = range(4)



def start_callback(update: Update, context):
    user.add_user(update.effective_user['id'], serialize_datetime(datetime.today()))
    reply_keyboard = [['Men', 'Women']]
    update.message.reply_text(
        'Добро пожаловать в естьбот!'
        'Это бот, который поможет вам контроллировать ваше питание'
        'Для инициализации вашей программы питания нужнно ввести ваши начальные показатели'
        'Введите ваш пол: ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SEX

def sex_callback(update, context):
    def define_sex(text: str) -> bool:
        if text == 'Men':
            return True
        elif text == 'Women':
            return False

    logger.info("Gender of %s: %s", update.message.from_user.first_name, update.message.text)
    user.set_user_sex(update.effective_user['id'], define_sex(update.message.text))
    update.message.reply_text('Введите ваш возраст: ')
    return AGE

def age_callback(update: Update, context):
    logger.info("Age of %s: %s", update.message.from_user.first_name, update.message.text)
    user.set_user_age(update.effective_user['id'], int(update.message.text))
    update.message.reply_text('Введите ваш рост: ')
    return HEIGHT

def height_callback(update, context):
    logger.info("Height of %s: %s", update.message.from_user.first_name, update.message.text)
    user.set_user_height(update.effective_user['id'], int(update.message.text))
    update.message.reply_text('И последнее, введите ваш вес: ')
    return WEIGHT

def weight_callback(update, context):
    logger.info("Weight of %s: %s", update.message.from_user.first_name, update.message.text)
    user.set_user_weight(update.effective_user['id'], float(update.message.text))
    update.message.reply_text('Отлично, ваша программа сконфигурирована')
    return ConversationHandler.END

def cancel_callback(update, context):
    logger.info("User %s canceled the conversation.", update.message.from_user.first_name)
    update.message.reply_text('...',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def get_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('start', start_callback)],
        states={
            SEX: [MessageHandler(Filters.regex('^(Men|Women)$'), sex_callback)],
            AGE: [MessageHandler(Filters.regex('^(100|[1-9][0-9]?)$'), age_callback)],
            HEIGHT: [MessageHandler(Filters.regex('^(?:0|[1-9]\d{0,2})$'), height_callback)],
            WEIGHT: [MessageHandler(Filters.regex('^(?:0|[1-9]\d{0,2})$'), weight_callback)]
        },

        fallbacks=[CommandHandler('cancel', cancel_callback)]
    )