import unittest
from selenium import webdriver
import parsers.Tele2.page as page
from time import sleep
import re
# from selenium.webdriver.common.keys import Keys


class Tele2Parser(unittest.TestCase):

    def setUp(self):
        self.state_url = input_state()
        self.date, self.start_date, self.finish_date = input_dates()
        self.mail = input_mail()
        self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.driver_2 = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.driver.get("https://msk.tele2.ru/about/news-list")
        self.driver_2.get("https://msk.tele2.ru/about/news-list")

    def test(self):
        print("Test\n")

        main_page = page.MainPage(self.driver)
        assert main_page.is_title_matches()

        sleep(2)
        counter = 1
        last_page = int(self.driver_2.find_element_by_class_name('paging').find_elements_by_tag_name('a')[-2].text)

        while counter <= last_page:
            main_page = page.MainPage(self.driver)

            counter_2 = 0
            while counter_2 < 5:
                try:
                    links = main_page.search_links
                    break
                except:
                    counter_2 += 1
                    sleep(3)
                    continue

            if counter_2 == 5:
                raise Exception('Couldn\'t find links on page')

            news = []

            for link in links:
                news.append(link.get_attribute('href'))

            for new in news:
                self.driver_2.get(new)
                inner_counter = 0
                while inner_counter < 5:
                    try:
                        date = month_name_to_num(self.driver_2.find_element_by_xpath(
                            '//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[2]/span').text.split(
                            ' '))
                        title = self.driver_2.find_element_by_xpath(
                            '//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[2]/h1/span').text
                        article = self.driver_2.find_element_by_xpath(
                            '//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/div/div').text
                        print(date)
                        print(title)
                        print('--------------\n', article, '\n-------------\n')
                        break
                    except:
                        inner_counter += 1
                        sleep(2)
                        continue

                if inner_counter == 3:
                    raise Exception('Couldn\'t find new\'s info')

            if counter < last_page:
                self.driver.find_element_by_id('pagingNextLink').click()
                counter += 1
            else:
                break

    def tearDown(self):
        self.driver.close()


def month_name_to_num(date_lst):
    month_dict = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                  'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

    for key, value in month_dict.items():
        if key == date_lst[1]:
            date_lst[1] = value

    date = str(date_lst[0] + '.' + date_lst[1] + '.' + date_lst[2])

    return date


def input_state():
    print('Добро пожаловать в парсер !')
    for i, st in enumerate(states_dict.values(), start=1):
        print(i, st)

    flag = False
    while True:
        state_choice = int(input('\nВыберите номер нужного вам региона из списка выше: '))

        for i, st in enumerate(states_dict.keys(), start=1):
            if i == state_choice:
                state_url = st
                flag = True

        if flag:
            break
        else:
            print('Номер введён неверно!')

    return state_url


def input_dates():
    while True:
        pat = re.compile('[0123]\d{1}\.[01]\d{1}\.20\d{2}-[0123]\d{1}\.[01]\d{1}\.20\d{2}')

        while True:
            date = input('Введите поисковый период в формате дд.мм.гг-дд.мм.гг (например, 03.07.2019-26.11.2020): ')
            if pat.fullmatch(date):
                break
            else:
                print('Следуйте формату введения даты!\n')

        start_date = date.split('-')[0]
        finish_date = date.split('-')[1]

        pattern = re.compile('[0123]\d{1}\.[01]\d{1}\.20\d{2}')
        if pattern.fullmatch(start_date) and pattern.fullmatch(finish_date):
            if -1 < int(start_date.split('.')[0]) < 32 and -1 < int(finish_date.split('.')[0]) < 32:
                if -1 < int(start_date.split('.')[1]) < 13 and -1 < int(finish_date.split('.')[1]) < 13:
                    if -1 < int(start_date.split('.')[0]) < 32 and -1 < int(finish_date.split('.')[0]) < 32:
                        if int(start_date.split('.')[2]) < int(finish_date.split('.')[2]):
                            break
                        elif int(start_date.split('.')[2]) == int(finish_date.split('.')[2]):
                            if int(start_date.split('.')[1]) < int(finish_date.split('.')[1]):
                                break
                            elif int(start_date.split('.')[1]) == int(finish_date.split('.')[1]):
                                if int(start_date.split('.')[0]) < int(finish_date.split('.')[0]):
                                    break

        print('Даты были введены некорректно!')

    return date, start_date, finish_date


def input_mail():
    while True:
        mail = input('Введите свою электронную почту: ')
        if '@' in mail and '.' in mail and 'mail' in mail:
            break
        else:
            print('\nВозможно, вы ввели почту неверно')

    return mail


states_dict = {
        'https://msk.tele2.ru/about/news-list': 'Москва и МO',
        'https://spb.tele2.ru/about/news-list': 'Санкт-Петербург и Ленинградская область',
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

if __name__ == "__main__":
    unittest.main()
