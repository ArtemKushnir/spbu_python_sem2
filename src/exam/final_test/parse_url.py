import re
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class URLNode:
    url: str
    parent: Optional["URLNode"]

    def get_path(self) -> list[str]:
        path = []
        curr_node = self
        while curr_node.parent is not None:
            path.append(curr_node.url)
            curr_node = curr_node.parent
        path.append(curr_node.url)
        path.reverse()
        return path


class Parse:
    @staticmethod
    def get_text_page(url: str) -> str:
        try:
            return requests.get(url).text
        except requests.RequestException:
            raise ConnectionError("the server is not responding")

    def get_all_href(self, curr_url: URLNode, pattern: str = "^/wiki/") -> list[URLNode]:
        result = []
        url_page = self.get_text_page(curr_url.url)
        soup = BeautifulSoup(url_page, "html.parser")
        for link in soup.findAll("a", attrs={"href": re.compile(pattern)}):
            result.append(URLNode("https://en.wikipedia.org" + link.get("href"), curr_url))
        return result
