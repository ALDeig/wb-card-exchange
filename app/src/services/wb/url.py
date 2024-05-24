import re

PATTERN = re.compile(r"https://www.wildberries.ru/catalog/\d+/detail.aspx")


def check_url(url: str) -> bool:
    match = re.match(PATTERN, url)
    return match is not None


def get_article(url: str) -> int:
    """Из url достается артикул и приводится к int"""
    url_without_params = url.split("?")[0]
    digits = re.findall(r"\d+", url_without_params)
    return digits[0]

