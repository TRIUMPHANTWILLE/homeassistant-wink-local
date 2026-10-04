from homeassistant.components.diagnostics import async_redact_data
TO_REDACT={"token","ssh_password","ssh_private_key","Authorization"}
async def async_get_config_entry_diagnostics(hass,entry):
 data=hass.data["wink_local"][entry.entry_id]; return {"config":async_redact_data(dict(entry.data),TO_REDACT),"devices":[d.raw for d in data["coordinator"].data.values()]}
