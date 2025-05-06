from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    data = {
        'songId': query.get('id')
    }

    result = await request.create_request(
        method='POST',
        url='https://interface3.music.163.com/eapi/music/wiki/home/song/get',
        data=data,
        options={
            'crypto': 'eapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
            'url': '/api/song/play/about/block/page'
        }
    )

    if result.get('status') != 200:
        return result

    return result
