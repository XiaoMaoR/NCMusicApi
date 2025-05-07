from fastapi import FastAPI, HTTPException, Request, Response
from api.template import api
from utils.request_async import AsyncRequest
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from http.cookies import SimpleCookie
import importlib.util
import os
import sys
API_MODULES = {}
api_dir = os.path.join(os.path.dirname(__file__), 'api')
app = FastAPI()

class Api_Main(BaseModel):
    data: dict
    proxy: str | None = None
    realIP: str | None = None
    cookie: dict | None = None

def apply_cookies(response: Response, cookie_data):
    cookies = SimpleCookie()
    if isinstance(cookie_data, SimpleCookie):
        cookies = cookie_data
    elif isinstance(cookie_data, dict):
        for key, val in cookie_data.items():
            if isinstance(val, dict):
                morsel = cookies[key]
                morsel.set(key, val.get("value", ""), val.get("value", ""))
                for attr_key, attr_val in val.items():
                    morsel[attr_key.lower()] = str(attr_val)
            else:
                cookies[key] = val
    elif isinstance(cookie_data, str):
        cookies.load(cookie_data)
    for morsel in cookies.values():
        response.set_cookie(
            key=morsel.key,
            value=morsel.value,
            path=morsel['path'] or '/',
            expires=morsel['expires'] or None,
            max_age=int(morsel['max-age']) if morsel['max-age'] else None,
            secure=bool(morsel['secure']),
            httponly=bool(morsel['httponly']),
            samesite=morsel['samesite'] or None
        )

def load_module_from_file(filepath, module_name):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None:
        raise ImportError(f"Could not load spec for {module_name}")
    if spec.loader is None:
        raise ImportError(f"Could not get loader for {module_name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def load_api_modules():
    for filename in os.listdir(api_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f'api.{filename[:-3]}'
            filepath = os.path.join(api_dir, filename)
            try:
                module = load_module_from_file(filepath, module_name)
                if hasattr(module, 'api'):
                    api_name = filename[:-3]
                    API_MODULES[api_name] = module
                    print(f"Loaded API module: {api_name}")
            except Exception as e:
                print(f"Failed API module: {module_name}: {str(e)}")

@app.post("/api-post/{api_name}")
async def api_main(api_name: str, Api_Main: Api_Main, request: Request, response: Response, setCookie: bool = True):
    apim = api_name
    if apim not in API_MODULES:
        raise HTTPException(status_code=404, detail=f"API '{apim}' not found")
    try:
        module = API_MODULES[apim]
        async with AsyncRequest() as client:
            api_data = Api_Main.data.copy()
            if Api_Main.cookie is not None:
                api_data['cookie'] = Api_Main.cookie
            elif 'cookie' in request.headers:
                cookie_header = request.headers['cookie']
                cookie = SimpleCookie()
                cookie.load(cookie_header)
                api_data['cookie'] = {key: morsel.value for key, morsel in cookie.items()} # type: ignore
            else:
                api_data['cookie'] = {} # type: ignore
            if Api_Main.proxy is not None:
                api_data['proxy'] = Api_Main.proxy
            if Api_Main.realIP is not None:
                api_data['realIP'] = Api_Main.realIP
            result = await module.api(api_data, request=client)
            if setCookie and 'cookie' in result:
                cookie = result['cookie']
                apply_cookies(response, cookie)
            if setCookie == True:
                return result.get('body', {})
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/{api_name}")
async def get_api(api_name: str, request: Request, response: Response, setCookie: bool = True):
    api_data = dict(request.query_params)
    if api_name not in API_MODULES:
        raise HTTPException(status_code=404, detail=f"API '{api_name}' not found")
    try:
        module = API_MODULES[api_name]
        async with AsyncRequest() as client:
            if 'cookie' in request.headers:
                cookie_header = request.headers['cookie']
                cookie = SimpleCookie()
                cookie.load(cookie_header)
                api_data['cookie'] = {key: morsel.value for key, morsel in cookie.items()} # type: ignore
            else:
                api_data['cookie'] = {} # type: ignore
            if 'proxy' in api_data:
                api_data['proxy'] = api_data['proxy']
            if 'realIP' in api_data:
                api_data['realIP'] = api_data['realIP']
            else:
                api_data['realIP'] = request.client.host # type: ignore
            result = await module.api(api_data, request=client)
            if setCookie and 'cookie' in result:
                cookie = result['cookie']
                apply_cookies(response, cookie)
            if setCookie == True:
                return result.get('body', {})
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=PlainTextResponse)
async def index():
    api_list_text = "\n".join(API_MODULES.keys())
    return f"NCM-Api\nWelcome to the NCM-Api Server!\nBy XiaoMaoR\n\nAPI List:\n{api_list_text}\n\nQQ:1072755450"

if __name__ == "__main__":
    print(r"""  _  _  ___ __  __      _        _ 
 | \| |/ __|  \/  |___ /_\  _ __(_)
 | .` | (__| |\/| |___/ _ \| '_ \ |
 |_|\_|\___|_|  |_|  /_/ \_\ .__/_|
                           |_|     """)
    print("Loading API modules...")
    load_api_modules()
    print("Starting API server...")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=80)
