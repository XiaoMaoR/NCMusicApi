from typing import Optional, Dict, Any
from unittest import result
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    if 'key' not in query:
        return {
            'status': 400,
            'body': {
                'msg': '参数错误',
                'code': 400
            },
            'cookie': None
        }
    result = {
        'status': 200,
        "body": {
            'url': f'https://music.163.com/login?codekey={query.get('key')}',
            'qrurl': f"https://api.2dcode.biz/v1/create-qr-code?data=https://music.163.com/login?codekey={query.get('key')}",
            'code': 200
        },
        'cookie': None
    }
    return result