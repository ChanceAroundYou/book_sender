from typing import Any
from fastapi import Request


async def get_request_params(request: Request) -> dict[str, Any]:
    query_params = dict(request.query_params) or {}
    # query_params = {k: json.loads(v) for k, v in request.query_params.items()} or {}
    try:
        params = {**query_params, **(await request.json())}
    except Exception:
        params = query_params
        
    for k, v in params.items():
        if v == 'null':
            params[k] = None
        elif v == 'true':
            params[k] = True
        elif v == 'false':
            params[k] = False
        elif isinstance(v, str) and v.isdigit():
            params[k] = int(v)
        elif isinstance(v, str) and v.replace('.', '', 1).isdigit():
            params[k] = float(v)
    return params
