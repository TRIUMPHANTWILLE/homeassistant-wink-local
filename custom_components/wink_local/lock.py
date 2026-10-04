from homeassistant.components.lock import LockEntity
from .entity import WinkEntity
async def async_setup_entry(hass,entry,async_add_entities):
 d=hass.data["wink_local"][entry.entry_id]; c=d["coordinator"]; m=d["mapper"]; async_add_entities([WinkLock(c,entry.entry_id,i) for i,x in c.data.items() if m.platform_for(x)=="lock"])
class WinkLock(WinkEntity,LockEntity):
 @property
 def is_locked(self): return bool(self.device.state.get("locked"))
 async def async_lock(self,**kwargs): await self.coordinator.api.async_set_state(self.device_id,{"locked":True}); await self.coordinator.async_request_refresh()
 async def async_unlock(self,**kwargs): await self.coordinator.api.async_set_state(self.device_id,{"locked":False}); await self.coordinator.async_request_refresh()
