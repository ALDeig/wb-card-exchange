from app.src.services.wb.url import get_base_url_with_parts


def get_photo_url(scu: str) -> str:
    """Формирует url для загрузки фото товара."""
    base_url_with_parts = get_base_url_with_parts(scu)
    return f"{base_url_with_parts}/images/big/1.jpg"
