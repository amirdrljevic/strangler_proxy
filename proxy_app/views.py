# proxy_app/views.py

from django.http import HttpRequest, HttpResponse, JsonResponse
from .routing import get_target_backend
import httpx

def proxy_home(request: HttpRequest):
    # 1. Extract incoming request data
    incoming_path = request.path
    method = request.method
    # Clean headers to avoid conflicts with simple test servers
    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length", "accept-encoding", "connection")
    }
    body = request.body

    # 2. Lookup backend via our stub rules
    target_base = get_target_backend(incoming_path)
    if not target_base:
        return JsonResponse({"error": "No matching routing rule"}, status=404)

    target_url = f"{target_base}{incoming_path}"

    # 3. Forward the request using httpx
    try:
        with httpx.Client() as client:
            resp = client.request(
                method=method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=10.0
            )
    except httpx.RequestError as exc:
        # 4a. Handle network errors
        return JsonResponse({"error": "Upstream request failed", "details": str(exc)}, status=502)

    # 4b. Return the upstream response
    return HttpResponse(
        content=resp.content,
        status=resp.status_code,
        content_type=resp.headers.get("content-type", "text/plain")
    )
