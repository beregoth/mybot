import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import ephem
import datetime

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')
# Настройки прокси
PROXY = {'proxy_url': settings.PROXY_URL,
        'urllib3_proxy_kwargs': {
            'username': settings.PROXY_USERNAME,
            'password': settings.PROXY_PASSWORD
    }
}
def greet_user(update, context):
    text = 'Вызван /start. Вы можете узнать созвездие, в котором сегодня находится планеты, вызвав /planet X, где X это название планеты на анг.языке'
    print(text)
    update.message.reply_text(text)

def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def planet(update, context):
    user_text = update.message.text.split()
    print(user_text)
    pl = user_text[1].capitalize()
    print(pl)
    time = ephem.Date(datetime.date.today())
    print(time)
    try:
        planet = getattr(ephem, pl)()
        planet.compute(time)
        res = ephem.constellation(planet)
        update.message.reply_text(f'Сегодня планета {pl} находится в созвездии {res}')
    except (AttributeError, TypeError):
        update.message.reply_text('Планета не найдена.')


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()