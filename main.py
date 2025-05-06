from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import importlib.util
import os
import sys
from utils.request_async import AsyncRequest

API_MODULES = {}
api_dir = os.path.join(os.path.dirname(__file__), 'api')
app = FastAPI()

class Api_Main(BaseModel):
    api: str
    data: dict
    proxy: str | None = None
    realIP: str | None = None
    cookie: dict | None = None

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

@app.post("/api-main")
async def api_main(Api_Main: Api_Main):
    apim = Api_Main.api
    if apim not in API_MODULES:
        raise HTTPException(status_code=404, detail=f"API '{apim}' not found")
    try:
        module = API_MODULES[apim]
        async with AsyncRequest() as client:
            api_data = Api_Main.data.copy()
            if Api_Main.cookie is not None:
                api_data['cookie'] = Api_Main.cookie
            if Api_Main.proxy is not None:
                api_data['proxy'] = Api_Main.proxy
            if Api_Main.realIP is not None:
                api_data['realIP'] = Api_Main.realIP
            result = await module.api(api_data, request=client)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/{api_name}")
async def get_api(api_name: str, request: Request):
    api_data = dict(request.query_params)
    if api_name not in API_MODULES:
        raise HTTPException(status_code=404, detail=f"API '{api_name}' not found")
    try:
        module = API_MODULES[api_name]
        async with AsyncRequest() as client:
            if 'cookie' in api_data:
                api_data['cookie'] = api_data['cookie']
            elif 'cookie' in request.headers:
                api_data['cookie'] = request.headers['cookie']
            else:
                api_data['cookie'] = {} # type: ignore
            if 'proxy' in api_data:
                api_data['proxy'] = api_data['proxy']
            if 'realIP' in api_data:
                api_data['realIP'] = api_data['realIP']
            result = await module.api(api_data, request=client)
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