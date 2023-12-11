import httpx

from root import settings

base_url = settings.bot.BASE_URL


async def get_or_create_user(user) -> None:
    url = f"{base_url}/user/get-or-create/"
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'telegram_id': user.id
    }
    httpx.post(url, data=context)


async def create_test_request(data) -> None:
    url = f"{base_url}/science/"
    context = {
        'name': data['test_name'],
        'size': data['test_size'],
        'keys': data['test_keys'],
        'author': data['author']
    }
    # http://127.0.0.1:8000/api/science/
    response = httpx.post(url, data=context)
    return response.json()
