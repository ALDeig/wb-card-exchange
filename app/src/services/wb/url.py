import re

PATTERN = re.compile(r"https://(www.|)wildberries.ru/catalog/\d+/detail.aspx")


def check_url(url: str) -> bool:
    """Проверяет соответствует ли переданный url, возможному url WB."""
    match = re.match(PATTERN, url)
    return match is not None


def get_article(url: str) -> int:
    """Из url достается артикул и приводится к int."""
    url_without_params = url.split("?")[0]
    digits = re.findall(r"\d+", url_without_params)
    return digits[0]


def get_base_url_with_parts(scu: str) -> str:
    return (
        f"https://{_get_basket_url(int(scu[:-5]))}.wb.ru/"
        f"vol{scu[:-5]}/"
        f"part{scu[:-3]}/"
        f"{scu}"
    )


def _get_basket_url(val: int) -> str:
    """Возвращает версию basket для загрузки фотографии."""
    baskets = {
        (0, 144): "01",
        (144, 288): "02",
        (288, 432): "03",
        (432, 720): "04",
        (720, 1008): "05",
        (1008, 1062): "06",
        (1062, 1116): "07",
        (1116, 1170): "08",
        (1170, 1314): "09",
        (1314, 1602): "10",
        (1602, 1656): "11",
        (1656, 1920): "12",
        (1920, 2046): "13",
        (2046, 2189): "14",
    }
    for range_, basket in baskets.items():
        if val in range(*range_):
            return f"basket-{basket}"
    return "basket-15"
