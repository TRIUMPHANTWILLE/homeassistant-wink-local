from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

class WinkRadio(StrEnum):
    ZIGBEE = "zigbee"
    ZWAVE = "zwave"
    LUTRON = "lutron"
    KIDDE = "kidde"
    HTTP = "http"
    UNKNOWN = "unknown"

@dataclass(slots=True)
class WinkDevice:
    device_id: str
    local_id: int
    name: str
    object_type: str
    radio: WinkRadio = WinkRadio.UNKNOWN
    manufacturer: str | None = None
    model: str | None = None
    connected: bool = False
    state: dict[str, Any] = field(default_factory=dict)
    desired_state: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def unique_id(self) -> str:
        return f"wink_{self.local_id}"

    @property
    def attributes(self) -> set[str]:
        return set(self.state) | set(self.desired_state)
