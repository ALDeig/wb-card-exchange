from httpx import AsyncClient

from app.src.services.wb.url import get_base_url_with_parts


async def get_card_name(scu: int) -> str:
    url = get_base_url_with_parts(str(scu))
    async with AsyncClient() as client:
        response = await client.get(f"{url}/info/ru/card.json")
        return response.json()["imt_name"]
