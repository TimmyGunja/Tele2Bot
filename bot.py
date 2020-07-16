import config
import os
import telebot
from telebot import types
from flask import Flask, request
from time import sleep


bot = telebot.TeleBot(config.TOKEN)

months_dict = {'январь': 31, 'февраль': 28, 'март': 31, 'апрель': 30, 'май': 31, 'июнь': 30,
                  'июль': 31, 'август': 31, 'сентябрь': 30, 'октябрь': 31, 'ноябрь': 30, 'декабрь': 31}

states_dict = {
        'https://msk.tele2.ru/about/news-list': 'Москва и МO',
        'https://spb.tele2.ru/about/news-list': 'Санкт-Петербург и Лен. область',
        'https://chelyabinsk.tele2.ru/about/news-list': 'Челябинская область',
        'https://rostov.tele2.ru/about/news-list': 'Ростовская область',
        'https://irkutsk.tele2.ru/about/news-list': 'Иркутская область',
        'https://ekt.tele2.ru/about/news-list': 'Свердловская область',
        'https://nnov.tele2.ru/about/news-list': 'Нижегородская область',
        'https://barnaul.tele2.ru/about/news-list': 'Алтайский край',
        'https://arh.tele2.ru/about/news-list': 'Архангельская область',
        'https://belgorod.tele2.ru/about/news-list': 'Белгородская область',
        'https://bryansk.tele2.ru/about/news-list': 'Брянская область',
        'https://vladimir.tele2.ru/about/news-list': 'Владимирская область',
        'https://volgograd.tele2.ru/about/news-list': 'Волгоградская область',
        'https://vologda.tele2.ru/about/news-list': 'Вологодская область',
        'https://voronezh.tele2.ru/about/news-list': 'Воронежская область',
        'https://eao.tele2.ru/about/news-list': 'Еврейская АО',
        'https://ivanovo.tele2.ru/about/news-list': 'Ивановская область',
        'https://kaliningrad.tele2.ru/about/news-list': 'Калининградская область',
        'https://kaluga.tele2.ru/about/news-list': 'Калужская область',
        'https://kamchatka.tele2.ru/about/news-list': 'Камчатский край',
        'https://kuzbass.tele2.ru/about/news-list': 'Кемеровская область',
        'https://kirov.tele2.ru/about/news-list': 'Кировская область',
        'https://kostroma.tele2.ru/about/news-list': 'Костромская область',
        'https://krasnodar.tele2.ru/about/news-list': 'Краснодарский край и Адыгея',
        'https://krasnoyarsk.tele2.ru/about/news-list': 'Красноярский край (кроме Норильска)',
        'https://norilsk.tele2.ru/about/news-list': 'Красноярский край (Норильск)',
        'https://kurgan.tele2.ru/about/news-list': 'Курганская область',
        'https://kursk.tele2.ru/about/news-list': 'Курская область',
        'https://lipetsk.tele2.ru/about/news-list': 'Липецкая область',
        'https://magadan.tele2.ru/about/news-list': 'Магаданская область',
        'https://murmansk.tele2.ru/about/news-list': 'Мурманская область',
        'https://novgorod.tele2.ru/about/news-list': 'Новгородская область',
        'https://novosibirsk.tele2.ru/about/news-list': 'Новосибирская область',
        'https://omsk.tele2.ru/about/news-list': 'Омская область',
        'https://orenburg.tele2.ru/about/news-list': 'Оренбургская область',
        'https://orel.tele2.ru/about/news-list': 'Орловская область',
        'https://penza.tele2.ru/about/news-list': 'Пензенская область',
        'https://perm.tele2.ru/about/news-list': 'Пермский край',
        'https://vladivostok.tele2.ru/about/news-lis': 'Приморский край',
        'https://pskov.tele2.ru/about/news-list': 'Псковская область',
        'https://buryatia.tele2.ru/about/news-list': 'Республика Бурятия',
        'https://karelia.tele2.ru/about/news-list': 'Республика Карелия',
        'https://komi.tele2.ru/about/news-list': 'Республика Коми',
        'https://mariel.tele2.ru/about/news-list': 'Республика Марий Эл',
        'https://mordovia.tele2.ru/about/news-list': 'Республика Мордовия',
        'https://kazan.tele2.ru/about/news-list': 'Республика Татарстан',
        'https://khakasia.tele2.ru/about/news-list': 'Республика Хакасия и Республика Тыва',
        'https://ryazan.tele2.ru/about/news-list': 'Рязанская область',
        'https://samara.tele2.ru/about/news-list': 'Самарская область',
        'https://saratov.tele2.ru/about/news-list': 'Саратовская область',
        'https://sakhalin.tele2.ru/about/news-list': 'Сахалинская область',
        'https://smolensk.tele2.ru/about/news-list': 'Смоленская область',
        'https://tambov.tele2.ru/about/news-list': 'Тамбовская область',
        'https://tver.tele2.ru/about/news-list': 'Тверская область',
        'https://tomsk.tele2.ru/about/news-list': 'Томская область',
        'https://tula.tele2.ru/about/news-list': 'Тульская область',
        'https://tyumen.tele2.ru/about/news-list': 'Тюменская область',
        'https://izhevsk.tele2.ru/about/news-list': 'Удмуртская Республика',
        'https://uln.tele2.ru/about/news-list': 'Ульяновская область',
        'https://hmao.tele2.ru/about/news-list': 'Ханты-Мансийский АО—Югра',
        'https://chelyabinsk.tele2.ru/about/news-lis': 'Челябинская область',
        'https://chuvashia.tele2.ru/about/news-list': 'Чувашская Республика',
        'https://yanao.tele2.ru/about/news-list': 'Ямало-Ненецкий АО',
        'https://yar.tele2.ru/about/news-list': 'Ярославская область',
        }

company = None
state = None
state_url = None
mail = None
date_start_month = None
date_start_day = None
date_start_year = None
date_finish_month = None
date_finish_day = None
date_finish_year = None


@bot.message_handler(commands=['start'])
def send_start(message):
    global company
    company = None
    bot.send_message(message.chat.id, "Добро пожаловать\nВыберите новостной источник кнопками ниже",
                     reply_markup=NewsCompaniesKeyboard())


@bot.message_handler(func=lambda message: message.text.lower() == 'tele2', content_types=['text'])
def choosed_tele2(message):
    global company
    company = 'tele2'
    answer = bot.send_message(message.chat.id, 'Выберите интересующий вас регион', reply_markup=Tele2StatesKeyboard())
    bot.register_next_step_handler(answer, tele2)


@bot.message_handler(func=lambda message: message.text.lower() == 'ведомости', content_types=['text'])
def choosed_vedomosti(message):
    global company
    company = 'ведомости'
    bot.send_message(message.chat.id, 'Парсер данного источника пока в разработке!')


@bot.message_handler(func=lambda message: message.text in states_dict.values(), content_types=['text'])
def tele2(message):
    global state, state_url
    state = message.text

    for key, value in states_dict.items():
        if state == value:
            state_url = key

    for glob in globals().keys():
        if glob != 'company' and glob != 'state' and glob != 'state_url':
            glob = None

    answer = bot.send_message(message.chat.id, 'Выберите начальную дату.\nМесяц: ', reply_markup=DateMonthKeyboard())
    bot.register_next_step_handler(answer, process_date_start_month)













"""DATE MESSAGES PROCESSING"""
@bot.message_handler(func=lambda message: message in months_dict.keys() and date_start_month is None, content_types=['text'])
def process_date_start_month(message):
    global date_start_month
    date_start_month = message.text
    answer = bot.send_message(message.chat.id, 'День: ', reply_markup=DateDayKeyboard(date_start_month))
    bot.register_next_step_handler(answer, process_date_start_day)


@bot.message_handler(func=lambda message: date_start_month is not None and date_start_day is None, content_types=['text'])
def process_date_start_day(message):
    global date_start_day
    date_start_day = message.text
    answer = bot.send_message(message.chat.id, 'Год: ', reply_markup=DateYearKeyboard())
    bot.register_next_step_handler(answer, process_date_start_year)


@bot.message_handler(func=lambda message: date_start_day is not None and date_start_year is None, content_types=['text'])
def process_date_start_year(message):
    global date_start_year
    date_start_year = message.text
    answer = bot.send_message(message.chat.id, 'Выберите конечную дату.\nМесяц: ', reply_markup=DateMonthKeyboard())
    bot.register_next_step_handler(answer, process_date_finish_month)


@bot.message_handler(func=lambda message: message in months_dict.keys() and date_start_month is not None, content_types=['text'])
def process_date_finish_month(message):
    global date_finish_month
    date_finish_month = message.text
    answer = bot.send_message(message.chat.id, 'День: ', reply_markup=DateDayKeyboard(date_finish_month))
    bot.register_next_step_handler(answer, process_date_finish_day)


@bot.message_handler(func=lambda message: date_finish_month is not None and date_finish_day is None, content_types=['text'])
def process_date_finish_day(message):
    global date_finish_day
    date_finish_day = message.text
    answer = bot.send_message(message.chat.id, 'Год: ', reply_markup=DateYearKeyboard())
    bot.register_next_step_handler(answer, process_date_finish_year)


@bot.message_handler(func=lambda message: date_finish_day is not None and date_finish_year is None, content_types=['text'])
def process_date_finish_year(message):
    global date_finish_year
    date_finish_year = message.text
    answer = bot.send_message(message.chat.id, 'Введите свою почту(на неё будет отправлено письмо с результатом) ')
    bot.register_next_step_handler(answer, process_mail)


@bot.message_handler(func=lambda message: '@' in message.text, content_types=['text'])
def process_mail(message):
    global company, state, mail, date_start_month, date_start_day, \
        date_start_year, date_finish_month, date_finish_day, date_finish_year

    mail = message.text
    bot.send_message(message.chat.id, 'Собираем данные воедино...\n')
    msg = str('Составлен следующий запрос: ' + '\nИсточник: ' + company + '\nРегион: ' + state + \
              '\nНачальная дата: ' + date_start_day + ' ' + date_start_month + '(a/я) ' + date_start_year + \
              '\nКонечная дата: ' + date_finish_day + ' ' + date_finish_month + '(a/я) ' + date_finish_year + \
              '\nПочта: ' + mail)

    bot.send_message(message.chat.id, msg)
    answer = bot.send_message(message.chat.id, 'Запрос составлен верно?', reply_markup=YesOrNoKeyboard())
    bot.register_next_step_handler(answer, process_checking)


@bot.message_handler(func=lambda message: message.text == 'Да, ошибок нет' or message.text == 'Нет, есть ошибка', content_types=['text'])
def process_checking(message):
    if message.text == 'Да, ошибок нет':
        bot.send_message(message.chat.id, 'Приступаем к парсингу данных...'
                                          '\nПо окончании работы файл будет выслан вам на почту, ждите!')


                #  ПРИКРУЧИВАЕМ СЮДА ПАРСЕР !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        import parsers.Tele2.main
        parse = parsers.Tele2.main.Tele2Parser()

    elif message.text == 'Нет, есть ошибка':
        bot.send_message(message.chat.id, 'Тогда начнем заново и повнимательнее'
                                          '\nВыберите новостной источник:', reply_markup=NewsCompaniesKeyboard())


@bot.message_handler(func=lambda message: True, content_types=['text'])
def process_message(message):
    bot.send_message(message.chat.id, message.text)




















"""KEYBOARDS"""
def NewsCompaniesKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Tele2'))
    keyboard.add(types.KeyboardButton('Ведомости'))
    return keyboard


def Tele2StatesKeyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for state in states_dict.values():
        keyboard.add(types.KeyboardButton(state))

    return keyboard


def DateMonthKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for month in months_dict.keys():
        keyboard.add(types.KeyboardButton(month))

    return keyboard


def DateDayKeyboard(month):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    num = months_dict.get(month)
    for n in range(1, num+1):
        keyboard.add(str(n))

    return keyboard


def DateYearKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    from time import asctime
    current_year = asctime().split()[-1]

    for year in range(2015, int(current_year)+1):
        keyboard.add(str(year))

    return keyboard


def YesOrNoKeyboard():
    keyboard = types.ReplyKeyboardMarkup()

    keyboard.add('Да, ошибок нет')
    keyboard.add('Нет, есть ошибка')

    return keyboard








if "HEROKU" in list(os.environ.keys()):
    server = Flask(__name__)

    @server.route('/' + config.TOKEN, methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=config.HEROKU_URL + config.TOKEN)
        return "!", 200

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
