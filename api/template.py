from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    data = {
        'key1': query.get('param1'),
        'key2': query.get('param2',"test"),
    }

    result = await request.create_request(
        method='POST',
        url='https://api.example.com/endpoint',
        data=data,
        options={
        'crypto': 'api',
        'cookie': query.get('cookie', {}),
        'proxy': query.get('proxy'),
        'realIP': query.get('realIP'),
    }
    )

    return result