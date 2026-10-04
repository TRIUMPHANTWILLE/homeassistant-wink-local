from __future__ import annotations

from .models import WinkDevice, WinkRadio

_RADIO_MAP = {0: WinkRadio.ZIGBEE, 1: WinkRadio.ZWAVE, 2: WinkRadio.LUTRON, 3: WinkRadio.KIDDE, 4: WinkRadio.HTTP}

class WinkDeviceMapper:
    def map_device(self, raw: dict) -> WinkDevice:
        state = raw.get("last_reading") or {}
        radio_raw = raw.get("radio_type")
        if isinstance(radio_raw, str):
            try:
                radio = WinkRadio(radio_raw.lower())
            except ValueError:
                radio = WinkRadio.UNKNOWN
        else:
            radio = _RADIO_MAP.get(radio_raw, WinkRadio.UNKNOWN)
        local_id = int(raw.get("local_id", raw.get("hub_device_id", -1)))
        return WinkDevice(
            device_id=str(raw.get("hub_device_id", local_id)), local_id=local_id,
            name=raw.get("name") or f"Wink device {local_id}", object_type=raw.get("object_type", "hub_device"),
            radio=radio, manufacturer=raw.get("device_manufacturer"), model=raw.get("model_name") or raw.get("manufacturer_device_model"),
            connected=bool(state.get("connection", False)), state=state, desired_state=raw.get("desired_state") or {}, raw=raw)

    def map_devices(self, raw_devices: list[dict]) -> dict[str, WinkDevice]:
        return {str(d.device_id): d for d in (self.map_device(x) for x in raw_devices)}

    def platform_for(self, device: WinkDevice) -> str | None:
        attrs=device.attributes
        name=device.name.lower()
        if device.local_id == 0:
            return None
        if "locked" in attrs:
            return "lock"
        if "powered" in attrs and "brightness" in attrs:
            return "light"
        if "powered" in attrs:
            return "switch"
        if any(k in attrs for k in ("alarm1", "alarm2", "tamper", "zone_status", "motion", "contact")) or "ias zone" in name:
            return "binary_sensor"
        if "battery" in attrs or "battery_voltage" in attrs:
            return "sensor"
        return "sensor"
