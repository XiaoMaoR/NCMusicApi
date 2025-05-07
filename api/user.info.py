from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest
import orjson

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    result = await request.create_request(
        method='POST',
        url=f'https://music.163.com/weapi/v1/user/detail/{query.get("id")}',
        data={},
        options={
            'crypto': 'weapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    result_bytes = orjson.dumps(result)
    replaced_bytes = result_bytes.replace(b'avatarImgId_str', b'avatarImgIdStr')

    result = orjson.loads(replaced_bytes)

    return result