import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
#import vk_api
import json
import lxml
import os

"""Задачи:
- user_agent
- proxy    
- cookies
- headless
- switch to window
- multiprocessing
"""

settings = input("Ожидание старта...введите 'S', если хотите изменить настройки: ").lower()
if settings == "s":
    settings = input("""Общие настройки:
    'NoobClub' - n
    WoWProgress - w
    Coins - c
    VK - v
    Telegram - t
    """)


class Selenium:

    test = "Процесс..."

    def __init__(self):
        options = Options()
        options.add_argument("--stars-maximized")
        self.driver = webdriver.Chrome(executable_path="D:\\Программы\\Py Project\\Seleniym\\venv\\chromedriver.exe",
                                       options=options)
        print("Создан объект: Selenium")

    def __str__(self):
        print("Selenium")

#p = 1
class News:

    input_guild = input("Введите название гильдии: ").title()
    input_text = input("Введите поиск по тегу: ")

    def __init__(self, name=input_guild, text=input_text):
        self.all_news = {
            "News": [{
                "NoobClub": {
                },
                "WoWProgress": [{
                    "Name - ItemLevel": {
                    },
                    "Leave: Name - Data - State": {
                    }
                }],
                "Coin_market_cap": {
                },
                "VK_API": {
                },
                "Telegram_API": {
                }
                }]
            }

        self.name_guild = name
        self.text = text

    def __str__(self):
        print("News")

    @staticmethod
    def create_dump():
        if os.path.exists(f"C:/Users/leorl/Desktop/All_News"):
            print("Папка уже существует!")
        else:
            os.mkdir(f"C:/Users/leorl/Desktop/All_News")

    def write_create_json(self):
        with open("NoobClub.json", "w", encoding="utf-8") as file:
            json.dump(self.all_news, file, indent=4, ensure_ascii=False)
        print("Файлы записаны!")


class NoobClub(News):

    def __init__(self, page=1, headlines=True):
        super().__init__()
        self.url = "https://www.noob-club.ru/"
        self.page = page
        self.block_post = []
        self.block_news = []
        self.headlines = headlines
        print("Создан объект: NoobClub")

    def __str__(self):
        print("NoobClub")
        print(self.text)

    def pars_news(self):
        if self.text == "":
            print(f"Собираю новости с {self.page} страниц NoobClub...")
        if self.text != "":
            print(f"Собираю новости с {self.page} страниц NoobClub с тегом: {self.text}...")
        number_page = 0
        for page in range(self.page):
            html_url = requests.get(self.url).text
            number_page = int(number_page) + 15
            self.url = "https://www.noob-club.ru/index.php?frontpage;p=" + str(number_page)
            soup = BeautifulSoup(html_url, "html.parser")
            soup_post = soup.find_all("h1")
            soup_news = soup.find_all("span", {"class": "entry-content"})
            for x in soup_post:
                self.block_post.append(x.text)
            for x in soup_news:
                self.block_news.append(x.text)

        num_news = 0
        if self.text == "":
            for x in self.block_post:
                if self.headlines:
                    news.all_news["News"][0]["NoobClub"][x] = self.block_news[num_news]
                    num_news += 1
                else:
                    news.all_news["News"][0]["NoobClub"][x] = ""
        else:
            for x in self.block_post:
                if self.headlines:
                    if self.text in x or self.text in self.block_news[num_news]:
                        news.all_news["News"][0]["NoobClub"][x] = self.block_news[num_news]
                        num_news += 1
                    else:
                        num_news += 1
                else:
                    if self.text in x:
                        news.all_news["News"][0]["NoobClub"][x] = ""

        print("Сбор новостей завершен!")


class WowProgress(News):

    def __init__(self, leave_page=1,):
        super().__init__()

        self.url_guild = f"https://www.wowprogress.com/guild/eu/гордунни/{self.name_guild}?roster"
        self.url_leave = "https://www.wowprogress.com/guild/eu/%D0%B3%D0%BE%D1%80%D0%B4%D1%83%D0%BD%D0%BD%D0%B8/%D" \
                         "0%AD%D0%B2%D0%B5%D0%BB%D0%B0%D0%BD%D1%88"
        self.leave_page = leave_page
        print("Создан объект: WowProgress")

    def __str__(self):
        print("WoWProgress")
        print(self.name_guild)

    def pars_news(self):

        """Парсер всех участников гильдии и их уровень экипировки"""

        print(f"{self.name_guild}: поиск участников гильдии и их уровня экипировки...")

        rec = requests.get(self.url_guild).text
        soup = BeautifulSoup(rec, "lxml")

        name = soup.find("table", {"class": "rating", "id": "char_list_table"})
        name = name.find_all("tr")

        player = soup.find("h2").text
        player = re.findall(r"(\d+)", player)

        news.all_news["News"][0]["WoWProgress"][0]["Name - ItemLevel"]["Количество персонажей"] = player[1]
        news.all_news["News"][0]["WoWProgress"][0]["Name - ItemLevel"]["Уникальных игроков"] = player[2]
        print(f"Найдено {player[1]} персонажей, {player[2]} уникальных игроков")

        for x in name:
            name_guild = str(x.find_all("td", limit=4))
            my_text = r'(\>\w+\<)'
            my_text_level = r'>[0-9]{3}.[0-9]{2}<'
            all_find_name = str(re.findall(my_text, name_guild))
            all_find_name = all_find_name[4:]
            all_find_level = str(re.findall(my_text_level, name_guild))
            all_find_name = re.findall(r"(\w+)", all_find_name)

            replace = ["[", "]", "<", ">"]
            for sim in replace:
                if sim in all_find_name:
                    all_find_name = all_find_name.replace(sim, "")

            all_find_level = str(re.findall(r"(\d+\.\d+)", all_find_level))

            all_find_name = str(all_find_name[0])
            all_find_level = (all_find_level[2:-2])

            news.all_news["News"][0]["WoWProgress"][0]["Name - ItemLevel"][all_find_name] = all_find_level

        print("Сбор информации об игроках завершен!")

        """Парсер покинувших/присоединившихся к гильдии"""

        print("Изменение ростера...")

        for x in range(self.leave_page):
            rec = requests.get(self.url_leave)
            rec = rec.text

            soup = BeautifulSoup(rec, "lxml")
            name = soup.find("ul", class_="eventList").find_all("li", class_="event")

            for item in name:
                try:
                    date = item.find("span", {"class": "eventDate"}).next_element.text
                    name_reider = item.find("a").next_element
                    state = item.find("a").next_element.next_element.strip()
                    news.all_news["News"][0]["WoWProgress"][0]["Leave: Name - Data - State"][f"{name_reider}"] = \
                        f"{date} - {state}"
                except:
                    pass

            next_name = soup.find("a", {"class": "navNext"})
            next_name_list = next_name.get("href")
            self.url_leave = "https://www.wowprogress.com" + next_name_list

        print("Изменения ростера собраны!")


class Coin(News):

    print(1*10)
    # sort_time = input("Введите тип сортировки по времени(24, 7): ").lower()
    # sort_max_min = input("Введите тип по росту(max, min): ").lower()
    print(2 * 10)

    def __init__(self):
        super().__init__()
        self.url_market = "https://coinmarketcap.com/"
        #self.sort_time = str(sort_time)
        #self.sort_max_min = str(sort_max_min)
        self.sort_time = input("Введите тип сортировки по времени(24, 7): ").lower()
        self.sort_max_min = input("Введите тип по росту(max, min): ").lower()

    def __str__(self):
        print("Coin_Market_Cap")

    def pars_news(self):

        print("Запрашиваю значения...")
        rec = requests.get(self.url_market).text
        soup = BeautifulSoup(rec, "lxml")

        all_coin = soup.find("tbody").find_all("tr", limit=10)

        massive = {}
        print("Ищу значения...")
        for item in all_coin:
            name_coin = item.find("p", {"font-weight": "semibold"}).text
            price = item.find("div", {"class": "sc-131di3y-0 cLgOOr"}).find("span").text
            price_24h_7d = item.find_all("span", {"class": ["sc-15yy2pl-0 kAXKAX", "sc-15yy2pl-0 hzgCfk"]})

            price_24 = price_24h_7d[0].text

            if "up" in str(price_24h_7d[0]):
                up_or_down_24 = "up"
            else:
                up_or_down_24 = "down"

            price_7d = price_24h_7d[1].text
            if "up" in str(price_24h_7d[1]):
                up_or_down_7d = "up"
            else:
                up_or_down_7d = "down"

            if self.sort_time == "24":
                price_24 = price_24.replace("%", "")
                massive[float(price_24)] = [name_coin, price, up_or_down_24, up_or_down_7d, price_7d]
            if self.sort_time == "7":
                price_7d = price_24.replace("%", "")
                massive[float(price_7d)] = [name_coin, price, up_or_down_24, price_24, up_or_down_7d]
        print("Сортирую значения...")
        if self.sort_max_min == "max":
            sorted_tuple = sorted(massive.items(), key=lambda x: x[0])
            sorted_tuple.reverse()
        if self.sort_max_min == "min":
            sorted_tuple = sorted(massive.items(), key=lambda x: x[0])
        else:
            print("Ошибка значения сортировки!!!")

        print("Добавляю значения в массив...")
        for item in sorted_tuple:
            time_24_or_7 = float(item[0])
            massive_coin = (massive[time_24_or_7])

            if self.sort_time == "24":
                news.all_news["News"][0]["Coin_market_cap"][massive_coin[0]] = [f"{massive_coin[1]}; 24 часа: "
                                                                                f"{massive_coin[2]} {str(time_24_or_7)}"
                                                                                f"%; 7 дней: {massive_coin[3]} "
                                                                                f"{massive_coin[4]}"]
            if self.sort_time == "7":
                news.all_news["News"][0]["Coin_market_cap"][massive_coin[0]] = [f"{massive_coin[1]}; 24 часа: "
                                                                                f"{massive_coin[2]} {massive_coin[3]}"
                                                                                f"%; 7 дней: {massive_coin[4]} "
                                                                                f"{str(time_24_or_7)}"]


class VK(News):

    def __init__(self):
        super().__init__()
        self.group_name = "igm"
        self.count = "10"
        self.token = "2c285c8e87ad770b2e7804d572e33d054f08c7e4cfad2631fb18bcbf124a21edec2609729a0cfcfc011a2"
        self.url = f"https://api.vk.com/method/wall.get?domain={self.group_name}&count={self.count}&access_token={self.token}&v=5.81"

        """Пример ссылки для запроса токена
        "https://oauth.vk.com/authorize?client_id=8075048&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=notify,audio,wall,friends,groups,offline&response_type=token&v=5.131"
        """

    def __str__(self):
        print("Создан объект: VK")

    def vk_pars(self):
        rec = requests.get(self.url).json()

        # with open("TEST.json", "w", encoding="utf-8") as file:
        #     json.dump(rec, file, indent=4, ensure_ascii=False)

        post = rec["response"]["items"]
        print(post)

        for x in post:
            post_news = x["likes"]["count"]
            print(post_news)

    def vk_api(self):
        print(1)


if __name__ == "__main__":
    print(Selenium.test)

news = News()
#
noob = NoobClub(page=3, headlines=True)
noob.pars_news()
#
wowprogress = WowProgress(leave_page=5)
wowprogress.pars_news()
#
coin = Coin()
coin.pars_news()
#
news.create_dump()
news.write_create_json()
#
# vk = VK()
# vk.vk_pars()


"""
Мейн закрывашкой
ДОБАВИТЬ ИФЫ ЕСЛИ ЗНАЧЕНИЯ НЕ ВВЕДИНЫ!
Получение всех валют с первой страницы

Посты новостной ленты в вк через api
Зайти на страницу и спарсить свои сообщения через кукичи
Личные сообщения отправка себе

запись звука winsound
"""