import config
import sys
import telegram.bot
import logging
from mqwrapper import MQBot
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request
from user_conv_start import get_conv_handler



formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatstr)
logging.basicConfig(format=formatstr,level=logging.INFO)

logger = logging.getLogger(__name__)
filehandler = logging.FileHandler('log.log')
filehandler.setLevel(logging.INFO)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)





if __name__ == '__main__':
    # for test purposes limit global throughput to 3 messages per 3 seconds
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    # set connection pool size for bot
    request = Request(con_pool_size=8,
                      proxy_url=config.REQUEST_KWARGS['proxy_url'],
                      urllib3_proxy_kwargs=config.REQUEST_KWARGS['urllib3_proxy_kwargs'])
    mqbot = MQBot(config.TOKEN, request=request, mqueue=q)
    upd = telegram.ext.updater.Updater(bot=mqbot, use_context=True)


    upd.dispatcher.add_handler(get_conv_handler())

    upd.start_polling()