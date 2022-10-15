from functools import wraps
from http import HTTPStatus

import aiohttp
from src.core.config.settings import AUTH_SERVICE_URL
from fastapi import HTTPException


async def request(url, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as response:
                if response.status != HTTPStatus.OK:
                    message = await response.json()
                    raise HTTPException(
                        status_code=HTTPStatus.UNAUTHORIZED,
                        detail=message
                    )
                return response.json()
        except aiohttp.ServerConnectionError as e:
            # В случае возникновения 500 ошибки, предполагается,
            # что пользователь авторизован
            return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth_header = kwargs.get('authorization', None)
        if not auth_header:
            return {'message': 'Athorization headers are not provided.'}

        headers = {'authorization': auth_header}
        await request(AUTH_SERVICE_URL, headers=headers)

        result = await func(*args, **kwargs)
        return result
    return wrapper