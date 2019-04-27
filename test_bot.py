from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
import os
from sys import executable
from time import sleep
from telegram import ReplyKeyboardMarkup
import request
import requests
import json


TOKEN = "817991028:AAGSjEbvqmnv2FB3epcvVkrXHQ4q7WTf1s8"

def setup_proxy_and_start(token, proxy=True):
    # Указываем настройки прокси (socks5)
    address = "aws.komarov.ml"
    port = 1080
    username = "yandexlyceum"
    password = "yandex"

    # Создаем объект updater. В случае отсутствия пакета PySocks установим его
    try:

        updater = Updater(token, request_kwargs={'proxy_url': f'socks5://{address}:{port}/',
                                                 'urllib3_proxy_kwargs': {'username': username,
                                                                          'password': password}} if proxy else None)
        print('Proxy - OK!')

        # Запускаем бота
        main(updater)
    except RuntimeError:
        sleep(1)
        print('PySocks не установлен!')
        os.system(f'{executable} -m pip install pysocks --user')  # pip.main() не работает в pip 10.0.1

        print('\nЗавистимости установлены!\nПерезапустите бота!')
        exit(0)


def main(updater):
    dp = updater.dispatcher
    conv_hadler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, first_answer)],
            2: [MessageHandler(Filters.text, sknd_answer)],
            3: [MessageHandler(Filters.text, thrd_answer)],
            4: [MessageHandler(Filters.text, fourth_answer)],
            5: [MessageHandler(Filters.text, fifth_answer)],
            6: [MessageHandler(Filters.text, sixth_answer)],
            7: [MessageHandler(Filters.text, seventh_answer)],
            8: [MessageHandler(Filters.text, eighth_answer)],
            9: [MessageHandler(Filters.text, nine_answer)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_hadler)
    dp.add_handler(CommandHandler('toponim', toponim))
    dp.add_handler(MessageHandler(Filters.text, geocode))
    updater.start_polling()
    updater.idle()


def start(bot, update):
    reply_keyboard = [['да'], ['нет']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Хотите пройти тест на знание географии Росии?", reply_markup=markup)
    if update.message.text is 'нет':
        #update.message.reply_text(update.message.text)
        return ConversationHandler.END
    else:
        return 1

def stop(bot, update):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END

def geocode(bot, updater):
    print(211)
    geocoder_uri = geocoder_request_template = \
        "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "format": "json",
        "geocode": updater.message.text
    })
    toponym = response.json()["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta = "0.005"

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }

    ll = map_params['ll']
    spn = map_params['spn']

    static_api_request = \
        "http://static-maps.yandex.ru/1.x/?ll={}&spn={}&l=map".format(ll, spn)

    bot.sendPhoto(
        updater.message.chat.id,
        static_api_request
    )



def toponim(bot, update):
    update.message.reply_text("Введите название обьекта")
    geocode()

def first_answer(bot, update):
    reply_keyboard = [['якутия'], ['забайкальский край'],
                      ['тюменская область'], ['хабаровский край']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 1")
    update.message.reply_text("Какой регион России имеет самую большую площадь?",
                              reply_markup=markup)

    return 2

def sknd_answer(bot, update):
    if update.message.text != 'якутия':
        update.message.reply_text("Ответ не верный.")
    reply_keyboard = [['Чукоткий АО', 'Еврейская АО'],
                     ['Адыгея', 'Ненецкий АО']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 2")
    update.message.reply_text("В каком субьекте РФ всего 1 город и 1 район, а людей меньше 50000?",
                              reply_markup=markup)

    return 3

def  thrd_answer(bot, update):
    if update.message.text != 'Ненецкий АО':
        update.message.reply_text("Ответ не верный.")
    reply_keyboard = [['да'], ['нет']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 3")
    update.message.reply_text("Правда ли, что территория Красноярского края больше Саудовской Аравии?",
                              reply_markup=markup)

    return 4

def fourth_answer(bot, update):
    if update.message.text != 'да':
        update.message.reply_text("Ответ не верный.")
    reply_keyboard = [['Эстония', 'Латвия'],
                     ['Литва', 'Беларусь']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 4")
    update.message.reply_text("С каким государством у Псковской области нет общей границы?",
                              reply_markup=markup)


    return 5

def fifth_answer(bot, update):
    if update.message.text != 'Литва':
        update.message.reply_text("Ответ не верный.")
    reply_keyboard = [['Самара', 'Сызрань'],
                      ['Элиста', 'Казань']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 5")
    update.message.reply_text("Какой из этих городов не расположен на Волге?",
                              reply_markup=markup)


    return 6

def sixth_answer(bot, update):
    if update.message.text != 'Элиста':
        update.message.reply_text("Ответ не верный.")
    reply_keyboard = [['Урал', 'Обь'],
                      ['Дон', 'Печора']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 6")
    update.message.reply_text("Какая из этих рек самая крупная (по расходу воды)",
                              reply_markup=markup)
    
    return 7

def seventh_answer(bot, update):
    if update.message.text != 'Обь':
        update.message.reply_text("Ответ не верный.")
    reply_keyboard = [['Анапа', 'Сочи'],
                      ['Туапсе', 'Новороссийск']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 7")
    update.message.reply_text("Какой из этих городов России расположен в субтропическом климате?",
                              reply_markup=markup)

    return 8

def eighth_answer(bot, update):
    if update.message.text != 'Сочи':
        update.message.reply_text("Ответ не верный.")

    reply_keyboard = [['Монголия', 'Китай'],
                      ['Казахстан', 'Северная Корея']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Вопрос 8")
    update.message.reply_text("С каким государством у Республики Алтай нет общей границы?",
                              reply_markup=markup)


    return 9

def nine_answer(bot, update):
    if update.message.text != 'Северная Корея':
        update.message.reply_text("Ответ не верный.")
    update.message.reply_text("Спасибо за прохождение теста")
    return ConversationHandler.END

if __name__ == '__main__':
    #main()
    setup_proxy_and_start(token=TOKEN, proxy=True)
