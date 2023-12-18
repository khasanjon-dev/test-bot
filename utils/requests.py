import httpx

from root import settings

base_url = settings.bot.BASE_URL


async def get_or_create_user(user) -> dict:
    url = f"{base_url}/user/get-or-create/"
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'telegram_id': user.id
    }
    response = httpx.post(url, data=context)
    return response.json()


async def create_test_request(data) -> dict:
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

# async def check_answer(keys: str):
#     test_id, keys = keys.split('#')
#     url = f'{base_url}/science/18/'
#     keys = keys_serializer(keys)
#     keys_api =
