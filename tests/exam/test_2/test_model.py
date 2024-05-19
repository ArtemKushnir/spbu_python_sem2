import asyncio

import pytest
import requests

from src.exam.test_2.model import QuotesModel


class TestModel:
    model = QuotesModel()

    @pytest.mark.parametrize("quote_count", [5, 15, 25])
    def test_parse_last(self, quote_count):
        quotes = asyncio.run(self.model.parse(quote_count, ""))
        assert len(quotes) == quote_count

    @pytest.mark.parametrize("quote_count", [1, 2, 5])
    def test_parse_best(self, quote_count):
        quotes = asyncio.run(self.model.parse(quote_count, "best"))
        assert len(quotes) == quote_count

    @pytest.mark.parametrize("quote_count", [5, 15, 25])
    def test_parse_random(self, quote_count):
        quotes = asyncio.run(self.model.parse(quote_count, "random"))
        assert len(quotes) == quote_count

    @pytest.mark.parametrize(
        "url",
        [
            "https://xn--80abh7bk0c.xn--p1ai/",
            "https://xn--80abh7bk0c.xn--p1ai/best",
            "https://xn--80abh7bk0c.xn--p1ai/byrating",
        ],
    )
    def test_get_text_page(self, url):
        text = self.model.get_text_page(url)
        expected = requests.get(url).text
        assert text == expected

    @pytest.mark.parametrize("url", ["demo", "test", "fall"])
    def test_raise_exception(self, url):
        with pytest.raises(ConnectionError):
            self.model.get_text_page(url)
