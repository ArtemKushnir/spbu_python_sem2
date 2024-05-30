import pytest

from src.exam.final_test.main import *


@pytest.mark.parametrize(
    "url",
    [
        "https://en.wikipedia.org/wiki/Adolf_Hitler",
        "https://en.wikipedia.org/wiki/Germany",
        "https://en.wikipedia.org/wiki/Belgium",
    ],
)
def test_get_url_page(url):
    expected = requests.get(url).text
    actual = Parse().get_text_page(url)
    assert actual == expected


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (
            "https://en.wikipedia.org/wiki/Germany",
            "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ["https://en.wikipedia.org/wiki/Germany", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
        ),
        (
            "https://en.wikipedia.org/wiki/Struthas",
            "https://en.wikipedia.org/wiki/Ten_Thousand",
            [
                "https://en.wikipedia.org/wiki/Struthas",
                "https://en.wikipedia.org/wiki/Artaxerxes_II",
                "https://en.wikipedia.org/wiki/Ten_Thousand",
            ],
        ),
        (
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://en.wikipedia.org/wiki/Type_theory",
            [
                "https://en.wikipedia.org/wiki/Python_(programming_language)",
                "https://en.wikipedia.org/wiki/Type_system",
                "https://en.wikipedia.org/wiki/Type_theory",
            ],
        ),
    ],
)
def test_find_path_to_url(start, end, expected):
    bfs_finder = BFSWiki()
    actual = bfs_finder.find_path_two_url(start, end, 30)
    assert actual == expected


@pytest.mark.parametrize(
    "links,n_jobs,expected",
    [
        (
            ["https://en.wikipedia.org/wiki/Germany", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
            30,
            ["https://en.wikipedia.org/wiki/Germany", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
        ),
        (
            [
                "https://en.wikipedia.org/wiki/Dercylidas",
                "https://en.wikipedia.org/wiki/Corinthian_War",
                "https://en.wikipedia.org/wiki/Tanagra",
            ],
            60,
            [
                "https://en.wikipedia.org/wiki/Dercylidas",
                "https://en.wikipedia.org/wiki/Special:WhatLinksHere/Dercylidas",
                "https://en.wikipedia.org/wiki/Corinthian_War",
                "https://en.wikipedia.org/wiki/Corinth",
                "https://en.wikipedia.org/wiki/Tanagra",
            ],
        ),
        (
            [
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
                "https://en.wikipedia.org/wiki/Vladimir_Putin",
                "https://en.wikipedia.org/wiki/Belgium",
            ],
            100,
            [
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
                "https://en.wikipedia.org/wiki/Vladimir_Putin",
                "https://en.wikipedia.org/wiki/Mikhail_Mishustin",
                "https://en.wikipedia.org/wiki/Belgium",
            ],
        ),
    ],
)
def test_main_unique(links, n_jobs, expected):
    unique = True
    actual = main(links, n_jobs, unique)
    assert actual == expected


@pytest.mark.parametrize(
    "links,n_jobs,expected",
    [
        (
            ["https://en.wikipedia.org/wiki/Germany", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
            30,
            ["https://en.wikipedia.org/wiki/Germany", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
        ),
        (
            [
                "https://en.wikipedia.org/wiki/Dercylidas",
                "https://en.wikipedia.org/wiki/Corinthian_War",
                "https://en.wikipedia.org/wiki/Tanagra",
            ],
            60,
            [
                "https://en.wikipedia.org/wiki/Dercylidas",
                "https://en.wikipedia.org/wiki/Special:WhatLinksHere/Dercylidas",
                "https://en.wikipedia.org/wiki/Corinthian_War",
                "https://en.wikipedia.org/wiki/Corinth",
                "https://en.wikipedia.org/wiki/Tanagra",
            ],
        ),
        (
            [
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
                "https://en.wikipedia.org/wiki/Vladimir_Putin",
                "https://en.wikipedia.org/wiki/Belgium",
            ],
            100,
            [
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
                "https://en.wikipedia.org/wiki/Vladimir_Putin",
                "https://en.wikipedia.org/wiki/Mikhail_Mishustin",
                "https://en.wikipedia.org/wiki/Belgium",
            ],
        ),
    ],
)
def test_main_without_unique(links, n_jobs, expected):
    unique = False
    actual = main(links, n_jobs, unique)
    assert actual == expected
