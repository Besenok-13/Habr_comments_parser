# coding=utf-8
import re
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
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


#        for link in soup.find_all("a"):
#            try:
#                g_link = link.get("href")
#            except TypeError:
#                continue

#            if g_link and g_link.startswith("http") and "google" not in g_link:
#                with_quest.append(unquote(g_link))

#        return with_quest
# adasd
# adasad
# asdadads


i = 1


def parser(url: str):
    ua = UserAgent()
    headers = {"accept": "*/*", "user-agent": ua.firefox}

    def gen_tree(soup):
        soup1 = soup.contents
        for j in soup1:
            comm_tag = j.find("div", {"xmlns": "http://www.w3.org/1999/xhtml"})
            if comm_tag:
                global i
                i += 1
                out.write(
                    str(i) + "*__*-*__*" + comm_tag.get_text().replace("\n", "") + "\n"
                )

                # print(str(i) + "*__*-*__*" + comm_tag.get_text())

                childs = j.find_all("div", {"class": "tm-comment-thread__children"})

                if childs:
                    # сделать параметр с минусом
                    gen_tree(childs[0])
                    # for child in childs:
                    #   gen_tree(child)

    def find_comments_trees(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(1)
            soup = bs(response.text, "html5lib")
            # soup = soup.find_all("div", {"class": "tm-comment__body-content"})
            links = soup.find_all("section", {"class": "tm-comment-thread"})
            # print(soup)
            for tree in links:
                pass
            return soup
        print("FAIL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None

    def without_post(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(1)
            soup = bs(response.text, "html5lib")
            soup = soup.find_all("div", {"class": "tm-comments__tree"})
            gen_tree(soup[0])
            # soup = soup.find_all("div", {"xmlns": "http://www.w3.org/1999/xhtml"})
            # print(soup)
            return soup
        return None

    with open("parsed.txt", "w", encoding="utf-8") as out:
        links = without_post(url, headers)
        # for name in links:
        # f_obj.write(name.prettify())
        #    out.write(name.get_text() + "\n")
        # f_obj.write("\n")


# Вставьте свой url
url = "https://habr.com/ru/post/490820/comments/"
parser(url)
