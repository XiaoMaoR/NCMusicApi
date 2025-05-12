from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

TYPE_MAP = {
    1: 1,      # 单曲
    2: 10,     # 专辑
    3: 100,    # 歌手
    4: 1000,   # 歌单
    5: 1002,   # 用户
    6: 1004,   # MV
    7: 1006,   # 歌词
    8: 1009,   # 电台
    9: 1014    # 视频
}

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    data = {
        's': query.get('keywords'),
        'type': TYPE_MAP.get(int(query.get('type', "song")), 1),
        'limit': query.get('limit', 30),
        'offset': query.get('page', 0),
    }

    result = await request.create_request(
        method='POST',
        url='https://music.163.com/weapi/search/get',
        data=data,
        options={
            'crypto': 'weapi',
            'cookie': query.get('cookie', {}),
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    return result