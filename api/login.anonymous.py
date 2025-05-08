from typing import Optional, Dict, Any
import base64
import hashlib
from utils.request_async import AsyncRequest

IDXORKEY = b'3go8&$833h0k(2)2'

def cloudmusic_dll_encode_id(some_id: str) -> str:
    xored = bytes([ord(c) ^ IDXORKEY[idx % len(IDXORKEY)] 
                  for idx, c in enumerate(some_id)])
    digest = hashlib.md5(xored).digest()
    return base64.b64encode(digest).decode()

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie'] = query.get('cookie', {})
    query['cookie']['os'] = 'iOS'

    device_id = 'NMUSIC'
    encoded_id = f'{device_id} {cloudmusic_dll_encode_id(device_id)}'
    username = base64.b64encode(encoded_id.encode()).decode()

    data = {
        'username': username,
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/register/anonimous',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query['cookie'],
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    if result['body']['code'] == 200:
        result = {
            'status': 200,
            'body': {
                **result['body'],
                'cookie': ';'.join(result['cookie']),
            },
            'cookie': result['cookie'],
        }

    return result