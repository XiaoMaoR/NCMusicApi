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
        'cp': False,
        'tv': 0,
        'lv': 0,
        'rv': 0,
        'kv': 0,
        'yv': 0,
        'ytv': 0,
        'yrv': 0
    }
    result = await request.create_request(
        method='POST',
        url='https://interface3.music.163.com/eapi/song/lyric/v1',
        data=data,
        options={
            'crypto': 'eapi',
            'cookie': query['cookie'],
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
            'url': '/api/song/lyric/v1'
        }
    )

    if result.get('status') != 200:
        return result

    return result