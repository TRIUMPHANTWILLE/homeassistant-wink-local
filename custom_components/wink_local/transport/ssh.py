from __future__ import annotations

import asyncssh

class WinkSSHError(Exception):
    pass

class WinkSSHClient:
    def __init__(self, host: str, port: int = 22, username: str = "root", password: str | None = None, private_key: str | None = None) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key

    async def _run(self, command: str) -> str:
        kwargs = {"host": self.host, "port": self.port, "username": self.username, "known_hosts": None}
        if self.password:
            kwargs["password"] = self.password
        if self.private_key:
            kwargs["client_keys"] = [self.private_key]
        try:
            async with asyncssh.connect(**kwargs) as connection:
                result = await connection.run(command, check=True, timeout=180)
                return result.stdout.strip()
        except (asyncssh.Error, OSError) as err:
            raise WinkSSHError(str(err)) from err

    async def start_pairing(self, radio: str, timeout: int = 60) -> str:
        if radio not in {"zigbee", "zwave", "lutron", "kidde", "http"}:
            raise WinkSSHError("unsupported radio")
        return await self._run(f"aprontest -a {int(timeout)} -r {radio}")
    async def start_exclusion(self, timeout: int = 60) -> str:
        return await self._run(f"timeout {int(timeout)} aprontest --zwave_exclusion_mode")
    async def refresh(self, master_id: int) -> str:
        return await self._run(f"aprontest -e -m {int(master_id)}")
    async def reconfigure(self, master_id: int) -> str:
        return await self._run(f"aprontest -E -m {int(master_id)}")
    async def remove(self, master_id: int, force: bool = False) -> str:
        op = "-f" if force else "-d"
        return await self._run(f"aprontest {op} -m {int(master_id)}")
    async def rename(self, master_id: int, name: str) -> str:
        safe = name.replace("'", "'\''")
        return await self._run(f"aprontest --set-name '{safe}' -m {int(master_id)}")
