from __future__ import annotations

import asyncio
import json
import ssl
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession, ClientTimeout

class WinkAAUError(Exception):
    pass
class WinkAAUAuthError(WinkAAUError):
    pass
class WinkAAUTokenExpired(WinkAAUAuthError):
    pass

class WinkAAUClient:
    def __init__(self, session: ClientSession, host: str, port: int, token: str, verify_ssl: bool = False) -> None:
        self.session = session
        self.base_url = f"https://{host}:{port}"
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = ClientTimeout(total=15)

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def _ssl(self):
        if self.verify_ssl:
            return None
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    async def _request(self, method: str, path: str, payload: Any | None = None) -> Any:
        try:
            async with self.session.request(method, self.base_url + path, headers=self.headers, json=payload, ssl=self._ssl(), timeout=self.timeout) as response:
                text = await response.text()
                if response.status == 401 and "tokens expired" in text.lower():
                    raise WinkAAUTokenExpired(text)
                if response.status in (401, 403):
                    raise WinkAAUAuthError(text)
                response.raise_for_status()
                if not text:
                    return {}
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return text
        except (ClientError, asyncio.TimeoutError) as err:
            if isinstance(err, (WinkAAUAuthError, WinkAAUTokenExpired)):
                raise
            raise WinkAAUError(str(err)) from err

    async def async_heartbeat(self):
        return await self._request("GET", "/heartbeat")
    async def async_hub_info(self):
        return await self._request("GET", "/hubs/me")
    async def async_get_devices(self):
        result = await self._request("GET", "/devices")
        return result.get("data", []) if isinstance(result, dict) else []
    async def async_get_device(self, device_id: str):
        result = await self._request("GET", f"/devices/{device_id}")
        data = result.get("data", []) if isinstance(result, dict) else []
        return data[0] if isinstance(data, list) and data else result
    async def async_set_state(self, device_id: str, desired_state: dict[str, Any], name: str | None = None):
        payload: dict[str, Any] = {"desired_state": desired_state}
        if name is not None:
            payload["name"] = name
        return await self._request("PUT", f"/devices/{device_id}", payload)
    async def async_run_scene(self, scene: list[dict[str, Any]]):
        return await self._request("POST", "/scenes/inline", {"scene": scene})
