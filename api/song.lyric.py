from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie']['os'] = 'ios'

    data = {
        'id': query['id'],
        'tv': -1,
        'lv': -1,
        'rv': -1,
        'kv': -1,
    }
    
    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/song/lyric?_nmclfl=1',
        data=data,
        options={
            'crypto': 'api',
            'cookie': query['cookie'],
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    if result.get('status') != 200:
        return result

    return result