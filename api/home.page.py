from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie'] = query.get('cookie', {})
    query['cookie']['os'] = query['cookie'].get('os', 'ios')
    query['cookie']['appver'] = query['cookie'].get('appver', '8.10.90')

    data = {
        'refresh': query.get('refresh', False),
        'cursor': query.get('cursor')
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/homepage/block/page',
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