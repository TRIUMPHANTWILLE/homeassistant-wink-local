from homeassistant.components.sensor import SensorEntity
from .entity import WinkEntity
async def async_setup_entry(hass,entry,async_add_entities):
 d=hass.data["wink_local"][entry.entry_id]; c=d["coordinator"]; m=d["mapper"]; async_add_entities([WinkDiagnostic(c,entry.entry_id,i) for i,x in c.data.items() if m.platform_for(x)=="sensor"])
class WinkDiagnostic(WinkEntity,SensorEntity):
 _attr_name="Status"
 @property
 def native_value(self): return "connected" if self.device.connected else "disconnected"
