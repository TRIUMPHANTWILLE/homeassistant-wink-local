from homeassistant.components.switch import SwitchEntity
from .entity import WinkEntity
async def async_setup_entry(hass, entry, async_add_entities):
 d=hass.data["wink_local"][entry.entry_id]; c=d["coordinator"]; m=d["mapper"]; async_add_entities([WinkSwitch(c,entry.entry_id,i) for i,x in c.data.items() if m.platform_for(x)=="switch"])
class WinkSwitch(WinkEntity,SwitchEntity):
 @property
 def is_on(self): return bool(self.device.state.get("powered"))
 async def async_turn_on(self,**kwargs): await self.coordinator.api.async_set_state(self.device_id,{"powered":True}); await self.coordinator.async_request_refresh()
 async def async_turn_off(self,**kwargs): await self.coordinator.api.async_set_state(self.device_id,{"powered":False}); await self.coordinator.async_request_refresh()
