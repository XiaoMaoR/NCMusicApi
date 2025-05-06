import time
from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    current_time = int(time.time() * 1000)
    data = {
        'startTime': query.get('startTime', current_time),
        'endTime': query.get('endTime', current_time)
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/mcalendar/detail',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    if result.get('status') != 200:
        return result

    return result
