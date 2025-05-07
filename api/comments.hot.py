from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

TYPE_MAP = {
    "0": "R_SO_4_",
    "1": "R_MV_5_",
    "2": "A_PL_0_",
    "3": "R_AL_3_",
    "4": "A_DJ_1_",
    "5": "R_VI_62_",
    "6": "A_EV_2_",
    "7": "A_DR_14_"
}

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie']['os'] = 'pc'
    resource_type = TYPE_MAP.get(query.get('type', '0'), 'R_SO_4_')
    data = {
        'rid': query.get('id'),
        'limit': query.get('limit', 20),
        'offset': query.get('offset', 0),
        'beforeTime': query.get('before', 0),
    }

    result = await request.create_request(
        method='POST',
        url=f'https://music.163.com/weapi/v1/resource/hotcomments/{resource_type}{query.get("id")}',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    return result