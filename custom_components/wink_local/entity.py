from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

class WinkEntity(CoordinatorEntity):
    _attr_has_entity_name=True
    def __init__(self, coordinator, entry_id: str, device_id: str) -> None:
        super().__init__(coordinator)
        self.entry_id=entry_id
        self.device_id=device_id
        self._attr_unique_id=f"{entry_id}_{device_id}"
    @property
    def device(self):
        return self.coordinator.data[self.device_id]
    @property
    def available(self):
        return super().available and self.device.connected
    @property
    def device_info(self):
        return DeviceInfo(identifiers={(DOMAIN, f"{self.entry_id}_{self.device_id}")}, name=self.device.name, manufacturer=self.device.manufacturer or "Wink", model=self.device.model or self.device.object_type, via_device=(DOMAIN, self.entry_id))
    @property
    def extra_state_attributes(self):
        return {"master_id": self.device.local_id, "radio": self.device.radio.value, "raw_state": self.device.state}
