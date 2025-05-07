from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    if 'cookie' not in query:
        query['cookie'] = {}
    query['cookie']['os'] = 'ios'
    query['cookie']['appver'] = '8.10.90'

    data = {
        'getcounts': True,
        'time': query.get('lasttime', -1),
        'limit': query.get('limit', 30),
        'total': False,
    }

    result = await request.create_request(
        method='POST',
        url=f'https://music.163.com/api/event/get/{query.get("id")}',
        data=data,
        options={
            'crypto': 'api',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    return result