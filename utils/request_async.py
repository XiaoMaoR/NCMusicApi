import asyncio
import orjson
import aiohttp
import random
import tempfile
import os
import time
from typing import Optional, Dict, Any
from urllib.parse import urlencode
from utils.crypto import random_string, weapi, linuxapi, eapi

class AsyncRequest:
    def __init__(self, max_concurrency=10):
        self._session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def __aenter__(self) -> "AsyncRequest":
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=0, force_close=True),
            json_serialize=lambda x: orjson.dumps(x).decode(),
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def _read_anonymous_token(self) -> str:
        token_path = os.path.join(tempfile.gettempdir(), 'anonymous_token')
        try:
            with open(token_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return 'anonymous_token'

    def _choose_user_agent(self, ua: Optional[str] = None) -> str:
        user_agent_list = {
            'mobile': [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.7 Mobile/15E148 Safari/605.1.15',
                'Mozilla/5.0 (Linux; Android 14; TECNO LI7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/27.0 Chrome/125.0.0.0 Mobile Safari/537.3'
            ],
            'pc': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6360.68 Safari/537.36 Edg/124.0.6360.68',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
            ],
        }
        if ua is None:
            real_list = user_agent_list['mobile'] + user_agent_list['pc']
        else:
            real_list = user_agent_list.get(ua, user_agent_list['mobile'] + user_agent_list['pc'])
        if ua in ('mobile', 'pc'):
            return random.choice(real_list)
        elif isinstance(ua, str) and ua:
            return ua
        else:
            return random.choice(real_list)

    async def create_request(
        self,
        method: str,
        url: str,
        data: Dict[str, Any] = {},
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        async with self.semaphore:
            options = options or {}
            cookies = options.get('cookie') or {}
            headers = {'User-Agent': self._choose_user_agent(options.get('ua'))}
            
            if 'headers' in options:
                headers.update(options['headers'])
            if method.upper() == 'POST':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            if 'music.163.com' in url:
                headers['Referer'] = 'https://music.163.com'

            ip = options.get('realIP') or options.get('ip')
            if ip:
                headers['X-Real-IP'] = ip
                headers['X-Forwarded-For'] = ip

            if isinstance(cookies, dict):
                cookies.setdefault('__remember_me', 'true')
                cookies.setdefault('_ntes_nuid', random_string())
                if 'login' not in url:
                    cookies.setdefault('NMTID', random_string())
                if 'MUSIC_U' not in cookies:
                    cookies.setdefault('MUSIC_A', await self._read_anonymous_token())
                    cookies.setdefault('os', 'ios')
                    cookies.setdefault('appver', '8.10.90')

            crypto = options.get('crypto')
            if crypto == 'weapi':
                data['csrf_token'] = cookies.get('__csrf', '')
                data = weapi(data)
                url = url.replace('/api', '/weapi')
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69'
            elif crypto == 'linuxapi':
                data = linuxapi({
                    'method': method,
                    'url': url.replace('/api', '/api'),
                    'params': data
                })
                headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
                url = 'https://music.163.com/api/linux/forward'
            elif crypto == 'eapi':
                csrf_token = cookies.get('__csrf', '')
                eapi_headers = {
                    'osver': cookies.get('osver'),
                    'deviceId': cookies.get('deviceId'),
                    'appver': cookies.get('appver', '8.9.70'),
                    'versioncode': cookies.get('versioncode', '140'),
                    'mobilename': cookies.get('mobilename'),
                    'buildver': cookies.get('buildver', str(int(time.time()))[:10]),
                    'resolution': cookies.get('resolution', '1920x1080'),
                    '__csrf': csrf_token,
                    'os': cookies.get('os', 'android'),
                    'channel': cookies.get('channel'),
                    'requestId': f"{int(time.time() * 1000)}_{random.randint(0, 9999):04d}"
                }
                if 'MUSIC_U' in cookies:
                    eapi_headers['MUSIC_U'] = cookies['MUSIC_U']
                if 'MUSIC_A' in cookies:
                    eapi_headers['MUSIC_A'] = cookies['MUSIC_A']
                headers['Cookie'] = '; '.join(f'{k}={v}' for k, v in eapi_headers.items())
                data['header'] = eapi_headers
                data = eapi(options.get('url', url), data)
                url = url.replace('/api', '/eapi')

            try:
                if self._session is None:
                    raise RuntimeError("Session is not initialized")
                
                request_fn = self._session.post if method.upper() == 'POST' else self._session.get
                data_param = urlencode(data) if method.upper() == 'POST' else data
                
                async with request_fn(url, data=data_param, headers=headers, cookies=cookies) as resp:
                    content_type = resp.headers.get('Content-Type', '').lower()
                    if 'application/json' in content_type:
                        body = await resp.json(loads=orjson.loads)
                    elif 'text/plain' in content_type:
                        text = await resp.text()
                        try:
                            body = orjson.loads(text)
                        except orjson.JSONDecodeError:
                            return {
                                'status': 502,
                                'msg': f"Failed to decode JSON from text/plain response: {text}"
                            }
                    else:
                        return {
                            'status': 502,
                            'msg': f"Unexpected Content-Type: {content_type}"
                        }
                    
                    status = int(body.get('code', 500))
                    if status in {201, 302, 400, 502, 800, 801, 802, 803}:
                        status = 200
                    
                    return {
                        'status': status,
                        'body': body,
                        'cookie': list(resp.cookies)
                    }
                    
            except Exception as e:
                return {
                    'status': 502,
                    'msg': str(e)
                }

    def remove_empty(self, data):
        if isinstance(data, dict):
            return {
                k: v for k, v in (
                    (k, self.remove_empty(v)) for k, v in data.items()
                ) if v not in (None, '', [], {})
            }
        elif isinstance(data, list):
            return [self.remove_empty(item) for item in data if item not in (None, '', [], {})]
        else:
            return data
