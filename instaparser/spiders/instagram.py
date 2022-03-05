import json
import re
from copy import deepcopy
from pprint import pprint
from urllib.parse import quote

import scrapy
from scrapy.http import HtmlResponse

from instaparser.items import InstaparserItem

# https://www.instagram.com/graphql/query/
# ?query_hash=8c2a529969ee035a5063f2fc8602a0fd
# &variables=%7B%22id%22%3A%2227790688603%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFBUS1lVHhvSHBZenR2S3c1ZGFzV2tPazVPTTY1Y0JLekdnSHdKbkZUN3FzbzRMMkZKMi1lRnlEczdFRFJYSXUwWk1fMWNRdHc4Mll1M1pQT0FZQXFkOA%3D%3D%22%7D


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    max_page_number = 3
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    username = "dedparser"
    enc_pass = (
        "#PWD_INSTAGRAM_BROWSER:10:1646481443"
        ":AatQAPgt5gvABFGzIW48XOFWj/2EgLYerWe"
        "ejN9hsNj4wxkxJlQkwhQwAZqFt0m9BbcxtgI"
        "i/sdQDUo8oMU4mE/2u6yUO6eW+uQ2G7cBicr"
        "x2OpBc3NXOmhbA553RAHqXFWFkvDoxGHG2Ct"
        "DcTP7lF5I"
    )
    user_to_parse_url_template = "/%s"
    user_to_parse = "machinelearning"
    posts_hash = "32b14723a678bd4628d70c1f877b94c9"
    graphql_url = "https://www.instagram.com/graphql/query/?"

    def parse(self, response: HtmlResponse, **kwargs):
        if response.status != 200:
            print(f"Запрос вернул статус = {response.status}")
            return

        print()
        csrf_token = self.fetch_csrf_token(response.text)
        instagram_ajax = self.fetch_instagram_ajax(response.text)
        cookie_string = response.headers["Set-Cookie"].decode()
        cookie_dict = dict(
            map(lambda x: x.strip().split("="), cookie_string.split(";")[:-1])
        )
        headers = {
            "x-instagram-ajax": instagram_ajax,
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "hmac.AR0m_dv4EN5"
            "Hs8bYWveq-qUICsK"
            "wNTJd8sg9FmNQ3rtzN2h1",
            "x-csrftoken": csrf_token,
        }
        form_data = {"username": self.username, "enc_password": self.enc_pass}
        yield scrapy.FormRequest(
            self.login_url,
            method="POST",
            callback=self.user_login,
            formdata=form_data,
            headers=headers,
            cookies=cookie_dict,
        )

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text: str):
        matched = re.search('"csrf_token":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    # Получаем instagram ajax заголовок
    def fetch_instagram_ajax(self, text: str):
        matched = re.search('"rollout_hash":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    def user_login(self, response: HtmlResponse):
        if response.status != 200:
            print(f"Запрос вернул статус = {response.status}")
            return

        data = response.json()
        print()
        if data["status"] != "ok":
            print("Произошла ошибка при логине")
            pprint(data)
            return

        if data["authenticated"]:
            yield response.follow(
                self.user_to_parse_url_template % self.user_to_parse,
                callback=self.user_data_parse,
                cb_kwargs={
                    "username": self.user_to_parse,
                },
            )

    def make_str_variables(self, variables: dict):
        str_variables = str(variables).replace(" ", "").replace("'", '"')
        return quote(str_variables)

    def user_data_parse(self, response: HtmlResponse, username: str):
        print()
        user_id = self.fetch_user_id(response.text, username)
        variables = {"first": 12, "id": user_id}
        str_variables = self.make_str_variables(variables)
        # print("$$$")
        url = (
            f"{self.graphql_url}"
            f"query_hash={self.posts_hash}"
            f"&variables={str_variables}"
        )
        yield response.follow(
            url,
            callback=self.user_post_parse,
            cb_kwargs={
                "username": username,
                "user_id": user_id,
                # на будущее: изучите в чем отличие глубокого копирования
                "variables": deepcopy(variables),
            },
        )

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text: str, username: str):
        regexp = '{"id":"\\d+","username":"%s"}' % username
        matched = re.search(regexp, text).group()
        return json.loads(matched).get("id")

    def user_post_parse(
        self,
        response: HtmlResponse,
        username: str,
        user_id: str,
        variables: dict,
        page_number: int = 1,
    ):
        print()

        data = response.json()
        # наиболее предпочтительный вариант
        # try:
        info = data["data"]["user"]["edge_owner_to_timeline_media"]
        posts = info["edges"]
        # работа с постами
        for post in posts:
            item = InstaparserItem()
            item["user_id"] = user_id
            node = post["node"]
            item["photo"] = node["display_url"]
            item["likes"] = node["edge_media_preview_like"]["count"]
            item["post_data"] = node
            yield item

        page_info = info["page_info"]
        # if page_info["has_next_page"]:
        # стандартное условие и ограничение страниц для пагинации
        if page_info["has_next_page"] and page_number < self.max_page_number:
            variables["after"] = page_info["end_cursor"]
            str_variables = self.make_str_variables(variables)
            url = (
                f"{self.graphql_url}"
                f"query_hash={self.posts_hash}"
                f"&variables={str_variables}"
            )
            yield response.follow(
                url,
                callback=self.user_post_parse,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    # на будущее: изучите в чем отличие глубокого копирования
                    "variables": deepcopy(variables),
                    "page_number": page_number + 1,
                },
            )
