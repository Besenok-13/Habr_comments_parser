# coding=utf-8

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

i = 0


def parser(url: str):
    ua = UserAgent()
    headers = {"accept": "*/*", "user-agent": ua.firefox}

    def gen_tree(soup, current_pos):
        soup1 = soup.contents
        for j in soup1:
            comm_tag = j.find("article", {"class": "tm-comment-thread__comment"})
            comm_text = j.find("div", {"class": "tm-comment__body-content"})
            if comm_text:
                global i
                i += 1
                now_i = i

                # comm_tag_to_wright = comm_text.find(
                #    "div", {"xmlns": "http://www.w3.org/1999/xhtml"}
                # )

                parent = current_pos
                out.write(
                    str(i)
                    + "*__*-*__*(-_-)"
                    + comm_text.get_text().replace("\n", " ")
                    + "*__*-*__*(-_-)"
                    + f"{parent}"
                    + "\n"
                )

                childs = comm_tag.find_next_siblings(
                    "div", {"class": "tm-comment-thread__children"}
                )

                if childs:
                    for child in childs:
                        gen_tree(child, now_i)

    def without_post(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(1)
            soup = bs(response.text, "html5lib")
            soup = soup.find_all("div", {"class": "tm-comments__tree"})

            """
                ООБНОВИТЬ ОТКЛОНЕНИЕ ВОЗМОЖЕН БАГ ПРИ ПЕРЕЗАПУСКЕ ЦИКЛА
            """
            if soup:
                gen_tree(soup[0], 0)
            # soup = soup.find_all("div", {"xmlns": "http://www.w3.org/1999/xhtml"})
            # print(soup)
        return i

    with open("parsed.txt", "a", encoding="utf-8") as out:
        links = without_post(url, headers)
        # for name in links:
        # f_obj.write(name.prettify())
        #    out.write(name.get_text() + "\n")
        # f_obj.write("\n")


# Вставьте свой url
for k in range(1, 349900):
    url = f"https://habr.com/ru/post/{k}/comments/"
    # https://habr.com/ru/post/490820/comments/
    parser(url)
