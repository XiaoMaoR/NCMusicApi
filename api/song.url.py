from typing import Optional, Dict, Any, List
import json
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie']['os'] = 'pc'
    ids = query.get('id', '').split(',')
    data = {
        'ids': json.dumps(ids),
        'br': int(query.get('br', 999000)),
    }

    result = await request.create_request(
        method='POST',
        url='https://interface3.music.163.com/eapi/song/enhance/player/url',
        data=data,
        options={
            'crypto': 'eapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
            'url': '/api/song/enhance/player/url',
        }
    )

    body = result.get('body', {})
    if 'data' in body:
        body['data'].sort(key=lambda x: ids.index(str(x['id'])))

    return result