from typing import Optional, Dict, Any
from utils.request_async import AsyncRequest

async def api(query: Dict[str, Any], request: Optional[AsyncRequest] = None):
    if request is None:
        async with AsyncRequest() as request:
            return await _api(query, request)
    return await _api(query, request)

async def _api(query: Dict[str, Any], request: AsyncRequest):
    query['cookie']['os'] = 'ios'

    data = {
        'id': query['id'],
        'tv': -1,
        'lv': -1,
        'rv': -1,
        'kv': -1,
    }
    
    result = await request.create_request(
        method='POST',
        url='https://music.163.com/api/song/lyric?_nmclfl=1',
        data=data,
        options={
            'crypto': 'api',
            'cookie': query['cookie'],
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
        }
    )

    body = result.get('body', {})

    return request.remove_empty({
        "status": result.get("status", None),
        "data": {
            "sgc_lyric": body.get("sgc", False),
            "instrumental": body.get("sfy", False),
            "multi_translated": body.get("qfy", False),
            "need_desclyric": body.get("needDesc", False),
            "pure_music": body.get("pureMusic", False),

            "translated_by": {
                "id": body.get("transUser", {}).get("id"),
                "user_id": body.get("transUser", {}).get("userid"),
                "nickname": body.get("transUser", {}).get("nickname"),
                "upload_time": body.get("transUser", {}).get("uptime"),
                "status": body.get("transUser", {}).get("status"),
            } if body.get("transUser") else None,

            "original_by": {
                "id": body.get("lyricUser", {}).get("id"),
                "user_id": body.get("lyricUser", {}).get("userid"),
                "nickname": body.get("lyricUser", {}).get("nickname"),
                "upload_time": body.get("lyricUser", {}).get("uptime"),
                "status": body.get("lyricUser", {}).get("status"),
            } if body.get("lyricUser") else None,

            "lyric": {
                "version": body.get("lrc", {}).get("version"),
                "content": body.get("lrc", {}).get("lyric"),
            },

            "lyric_cn": {
                "version": body.get("tlyric", {}).get("version"),
                "content": body.get("tlyric", {}).get("lyric"),
            },

            "lyric_kl": {
                "version": body.get("klyric", {}).get("version"),
                "content": body.get("klyric", {}).get("lyric"),
            },

            "lyric_rom": {
                "version": body.get("romalrc", {}).get("version"),
                "content": body.get("romalrc", {}).get("lyric"),
            },

            "lyric_": {
                "version": body.get("yrc", {}).get("version"),
                "content": body.get("yrc", {}).get("lyric"),
            }
        }
    })
