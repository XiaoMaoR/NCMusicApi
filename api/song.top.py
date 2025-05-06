from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie'] = query.get('cookie', {})
    query['cookie']['os'] = query['cookie'].get('os', 'pc')

    data = {
        'id': query.get('id'),
        'n': '500',
        's': '0'
    }

    result = await request.create_request(
        method='POST',
        url='https://interface3.music.163.com/api/playlist/v4/detail',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query['cookie'],
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    if result.get('status') != 200:
        return result

    return result