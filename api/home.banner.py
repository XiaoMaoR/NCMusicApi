from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

TYPE_MAP = {
    0: 'pc',
    1: 'android',
    2: 'iphone',
    3: 'ipad',
}

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):

    client_type = TYPE_MAP.get(query.get('type', 0), 'pc')

    data = {
        'clientType': client_type
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/v2/banner/get',
        data=data,
        options={
            'crypto': 'api',
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    if result.get('status') != 200:
        return result

    return result
