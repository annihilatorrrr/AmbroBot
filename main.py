import os
import logging
import re

from telegram.ext import (
    CommandHandler,
    Updater,
    Filters,
    MessageHandler,
    RegexHandler,
)
from commands import (
    dolar_hoy,
    partido,
    dolar_futuro,
    default,
    posiciones,
    link_ticket,
    subte,
    format_code,
    cartelera,
)
from command.tagger.all_tagger import (
    tag_all, set_all_members
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TICKET_REGEX = re.compile(r'((t|osp\-?)(?P<ticket>\d{5,6}))', re.IGNORECASE)
# Text starting with ~, \c, \code or $ will be monospaced formatted
CODE_PREFIX = re.compile(r'^(~|\\code|\$|\\c) (?P<code>[\s\S]+)')

# Setup bot
updater = Updater(os.environ['PYTEL'])
dispatcher = updater.dispatcher

# Add command handlers
partido_handler = CommandHandler('partido', partido)
dolar_handler = CommandHandler('dolar', dolar_hoy)
dolar_futuro_handler = CommandHandler('fdolar', dolar_futuro)
posiciones_handler = CommandHandler('posiciones', posiciones, pass_args=True)
subte_handler = CommandHandler('subte', subte)
cartelera_handler = CommandHandler('cartelera', cartelera)
code_handler = RegexHandler(CODE_PREFIX, format_code, pass_groupdict=True)
tag_all = MessageHandler(Filters.regex(r'@all'), tag_all)
edit_tag_all  = CommandHandler('setall', set_all_members, pass_args=True)
tickets_handler = RegexHandler(TICKET_REGEX, link_ticket, pass_groupdict=True)
generic_handler = MessageHandler(Filters.command, default)

#  Associate command with actions.
dispatcher.add_handler(dolar_handler)
dispatcher.add_handler(partido_handler)
dispatcher.add_handler(dolar_futuro_handler)
dispatcher.add_handler(posiciones_handler)
dispatcher.add_handler(subte_handler)
dispatcher.add_handler(cartelera_handler)
dispatcher.add_handler(tag_all)
dispatcher.add_handler(edit_tag_all)
dispatcher.add_handler(tickets_handler)
dispatcher.add_handler(code_handler)
dispatcher.add_handler(generic_handler)

updater.start_polling()
logger.info('Listening humans..')