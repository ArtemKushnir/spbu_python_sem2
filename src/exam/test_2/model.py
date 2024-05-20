import requests
from bs4 import BeautifulSoup

URL = "https://xn--80abh7bk0c.xn--p1ai/"
CNT_QUOTES = 10


class QuotesModel:
    @staticmethod
    def get_text_page(url: str) -> str:
        try:
            return requests.get(url).text
        except requests.RequestException:
            raise ConnectionError("the server is not responding")

    async def parse(self, cnt_quotes: int, name: str) -> list[str]:
        if name == "last":
            name = ""
        soup = BeautifulSoup(self.get_text_page(URL + name), "html.parser")
        for br in soup("br"):
            br.replace_with("\n")
        new_list = soup.findAll("div", class_="quote__body", limit=cnt_quotes)
        new_quotes = [quote.text.strip() for quote in new_list]
        return new_quotes
