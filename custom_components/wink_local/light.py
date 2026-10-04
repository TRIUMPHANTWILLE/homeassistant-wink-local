from __future__ import annotations
from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS
from .entity import WinkEntity
async def async_setup_entry(hass, entry, async_add_entities):
    data=hass.data["wink_local"][entry.entry_id]; c=data["coordinator"]; mapper=data["mapper"]
    async_add_entities([WinkLight(c, entry.entry_id, did) for did,d in c.data.items() if mapper.platform_for(d)=="light"])
class WinkLight(WinkEntity, LightEntity):
    _attr_color_mode=ColorMode.BRIGHTNESS; _attr_supported_color_modes={ColorMode.BRIGHTNESS}
    @property
    def is_on(self): return bool(self.device.state.get("powered"))
    @property
    def brightness(self):
        value=self.device.state.get("brightness")
        return round(float(value)*255) if value is not None else None
    async def async_turn_on(self, **kwargs):
        state={"powered":True}
        if ATTR_BRIGHTNESS in kwargs: state["brightness"]=max(0,min(255,kwargs[ATTR_BRIGHTNESS]))/255
        await self.coordinator.api.async_set_state(self.device_id,state); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.async_set_state(self.device_id,{"powered":False}); await self.coordinator.async_request_refresh()
