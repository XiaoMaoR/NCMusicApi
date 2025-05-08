from typing import Optional, Dict, Any, List
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    ids = [id.strip() for id in query.get('ids', '').split(',')]
    data = {
        'c': '[' + ','.join([f'{{"id":{id}}}' for id in ids]) + ']'
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/v3/song/detail',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    return result