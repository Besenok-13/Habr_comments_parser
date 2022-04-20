# coding=utf-8

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.firefox import GeckoDriverManager


class GoogleSearch:
    def __init__(self) -> None:
        self._firefox_options = webdriver.FirefoxOptions()
        self._firefox_options.add_argument("-headless")
        self._firefox_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.88 Safari/537.36"
        )

        self._driver = driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install()
        )

    def get_urls(self, q: str, start: int = 0):
        """
        Метод возвращает список url из Google запроса
        :param q: Запрос
               start: номер начальной страницы, начинается с 0
        :return: Список собранных url
        """

        # base_url = "https://www.google.com/search?q={}&start={}".format(q, start)
        base_url = q
        try:
            self._driver.get(base_url)
        except Exception as e:
            print(f"Ошибка {e} во время обработки")
            return []

        soup = bs(q, "lxml")
        print(soup.find_all("div", {"class": "tm-comments__tree"}))
        links = {}
        for i in soup.find_all("div", {"class": "tm-comments__tree"}):
            links.update({i.text: i.get("href")})
        return links
