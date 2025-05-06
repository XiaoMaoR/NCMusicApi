from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    data = {
        'ids': '[' + str(query.get('id')) + ']',
        'level': query.get('level', 'standard'),
        'encodeType': 'flac',
    }

    if data['level'] == 'sky':
        data['immerseType'] = 'c51'

    result = await request.create_request(
        method='POST',
        url='https://interface.music.163.com/eapi/song/enhance/player/url/v1',
        data=data,
        options={
            'crypto': 'eapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
            'url': '/api/song/enhance/player/url/v1',
        }
    )

    body = result.get('body', {})

    if result.get('status') != 200:
        return result

    return result