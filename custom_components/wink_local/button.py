from homeassistant.components.button import ButtonEntity
from .entity import WinkEntity
async def async_setup_entry(hass,entry,async_add_entities):
 d=hass.data["wink_local"][entry.entry_id]; c=d["coordinator"]; async_add_entities([WinkRefresh(c,entry.entry_id,i,d.get("ssh")) for i in c.data if int(c.data[i].local_id)!=0])
class WinkRefresh(WinkEntity,ButtonEntity):
 _attr_name="Refresh"
 def __init__(self,c,e,i,ssh): super().__init__(c,e,i); self.ssh=ssh
 async def async_press(self):
  if self.ssh: await self.ssh.refresh(self.device.local_id)
  await self.coordinator.async_request_refresh()
