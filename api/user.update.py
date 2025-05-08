from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie'] = query.get('cookie', {})
    query['cookie']['os'] = 'ios'
    query['cookie']['appver'] = '8.10.90'

    data = {
        'birthday': query.get('birthday'),
        'city': query.get('city'),
        'gender': query.get('gender'),
        'nickname': query.get('nickname'),
        'province': query.get('province'),
        'signature': query.get('signature'),
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/user/profile/update',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query['cookie'],
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    return result