from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    data = {
        'offset': query.get('offset', 0),
        'limit': query.get('limit', 30),
        'order': True,
    }

    result = await request.create_request(
        method='POST',
        url=f'https://music.163.com/weapi/user/getfollows/{query["id"]}',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    return result