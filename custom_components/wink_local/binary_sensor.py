from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from .entity import WinkEntity
async def async_setup_entry(hass,entry,async_add_entities):
 d=hass.data["wink_local"][entry.entry_id]; c=d["coordinator"]; m=d["mapper"]; async_add_entities([WinkBinary(c,entry.entry_id,i) for i,x in c.data.items() if m.platform_for(x)=="binary_sensor"])
class WinkBinary(WinkEntity,BinarySensorEntity):
 _attr_device_class=BinarySensorDeviceClass.OPENING
 @property
 def is_on(self):
  s=self.device.state
  return bool(s.get("alarm1") or s.get("alarm2") or s.get("motion") or s.get("contact") or s.get("zone_status",0))
