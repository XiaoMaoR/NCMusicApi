from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

import random
import string

def create_random_string(length: int) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie'] = query.get('cookie', {})
    query['cookie']['os'] = query['cookie'].get('os', 'pc')

    data = {
        'algorithmCode': 'shazam_v2',
        'times': 1,
        'sessionId': create_random_string(16),
        'duration': int(query.get('duration', 0)),
        'from': 'recognize-song',
        'decrypt': '1',
        'rawdata': query.get('audioFP')
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/music/audio/match',
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
