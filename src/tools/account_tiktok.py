from pathlib import Path
from re import compile

from lxml.etree import HTML

from src.DataAcquirer import Account
from src.DataAcquirer import Link

__all__ = ["TikTokAccount"]


class TikTokAccount:
    urls = "//*[@id=\"main-content-others_homepage\"]/div/div[2]/div[last()]/div/div/div/div/div/a/@href"
    uid = "//*[@id=\"main-content-others_homepage\"]/div/div[1]/div[1]/div[2]/div/div[2]/a/@href"
    uid_re = compile(r".*?u=(\d+).*?")
    nickname = "//*[@id=\"main-content-others_homepage\"]/div/div[1]/div[1]/div[2]/h2/text()"

    def __init__(self, path: str):
        self.path = Path(path.replace("\"", ""))

    def run(self) -> list:
        if self.path.is_file() and self.path.suffix == ".html":
            return self.__read_html_file([self.path])
        elif self.path.is_dir():
            return self.__read_html_file(self.path.glob("*.html"))
        return []

    def __read_html_file(self, items) -> list:
        ids = []
        for i in items:
            with i.open("r", encoding="utf-8") as f:
                data = f.read()
            ids.append(self.__extract_id_data(data))
        return [i for i in ids if all(i)]

    def __extract_id_data(self, html: str) -> (str, str, list[str]):
        html_tree = HTML(html)
        urls = html_tree.xpath(self.urls)
        uid = self.__extract_uid(html_tree.xpath(self.uid))
        nickname = self.__extract_nickname(html_tree.xpath(self.nickname))
        return uid, nickname, Link.works_link_tiktok.findall(" ".join(urls))

    def __extract_uid(self, text: list):
        if len(text) == 1:
            return u.group(1) if (
                u := self.uid_re.search(
                    text[0])) else Account.temp_data()
        return Account.temp_data()

    @staticmethod
    def __extract_nickname(text: list):
        if len(text) == 1:
            return text[0].strip() or Account.temp_data()
        return Account.temp_data()
