import config
import telegram.bot

from mqwrapper import MQBot
from telegram.ext import messagequeue as mq
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext
from telegram import Update, User
from telegram.utils.request import Request


if __name__ == '__main__':

    import os
    # for test purposes limit global throughput to 3 messages per 3 seconds
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    # set connection pool size for bot
    request = Request(con_pool_size=8,
                      proxy_url=config.REQUEST_KWARGS['proxy_url'],
                      urllib3_proxy_kwargs=config.REQUEST_KWARGS['urllib3_proxy_kwargs'])
    mqbot = MQBot(config.TOKEN, request=request, mqueue=q)
    upd = telegram.ext.updater.Updater(bot=mqbot, use_context=True)

    def reply(update, context):
        # tries to echo 10 msgs at once
        chatid = update.message.chat_id
        msgt = update.message.text
        print(msgt, chatid)
        for ix in range(10):
            context.bot.send_message(chat_id=chatid, text='%s) %s' % (ix + 1, msgt))

    def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
        print(update.effective_user)

    # hdl = MessageHandler(Filters.text, reply)
    # upd.dispatcher.add_handler(hdl)

    upd.dispatcher.add_handler(CommandHandler('start', start))

    upd.start_polling()