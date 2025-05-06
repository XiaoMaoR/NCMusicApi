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
        'cp': False,
        'tv': 0,
        'lv': 0,
        'rv': 0,
        'kv': 0,
        'yv': 0,
        'ytv': 0,
        'yrv': 0
    }
    result = await request.create_request(
        method='POST',
        url='https://interface3.music.163.com/eapi/song/lyric/v1',
        data=data,
        options={
            'crypto': 'eapi',
            'cookie': query['cookie'],
            'proxy': query.get('proxy'),
            'realIP': query.get('realIP'),
            'url': '/api/song/lyric/v1'
        }
    )

    if result.get('status') != 200:
        return result

    body = result.get('body', {})

    if body.get('lyric') == None and body.get('pureMusic') == None:
        return ({"status": 404,"msg": "该歌曲暂无歌词"})

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

            "lyric_romlrc": {
                "version": body.get("romalrc", {}).get("version"),
                "content": body.get("romalrc", {}).get("lyric"),
            },

            "lyric_": {
                "version": body.get("yrc", {}).get("version"),
                "content": body.get("yrc", {}).get("lyric"),
            }
        }
    })
