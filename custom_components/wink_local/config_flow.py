from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import *
from .transport.aau import WinkAAUClient, WinkAAUError
class WinkLocalConfigFlow(config_entries.ConfigFlow):
    VERSION = 1
    DOMAIN = DOMAIN
    VERSION=1
    async def async_step_user(self,user_input=None):
        errors={}
        if user_input is not None:
            try:
                api=WinkAAUClient(async_get_clientsession(self.hass),user_input[CONF_HOST],user_input[CONF_PORT],user_input[CONF_TOKEN],user_input[CONF_VERIFY_SSL])
                info=await api.async_hub_info(); await api.async_get_devices()
                await self.async_set_unique_id(user_input[CONF_HOST]); self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"Wink Hub {user_input[CONF_HOST]}",data=user_input)
            except WinkAAUError: errors["base"]="cannot_connect"
        schema=vol.Schema({vol.Required(CONF_HOST):str,vol.Required(CONF_PORT,default=DEFAULT_PORT):int,vol.Required(CONF_TOKEN):str,vol.Required(CONF_VERIFY_SSL,default=False):bool,vol.Optional(CONF_SCAN_INTERVAL,default=DEFAULT_SCAN_INTERVAL):int,vol.Optional(CONF_SSH_ENABLED,default=False):bool,vol.Optional(CONF_SSH_PORT,default=DEFAULT_SSH_PORT):int,vol.Optional(CONF_SSH_USER,default=DEFAULT_SSH_USER):str,vol.Optional(CONF_SSH_PASSWORD):str,vol.Optional(CONF_SSH_PRIVATE_KEY):str})
        return self.async_show_form(step_id="user",data_schema=schema,errors=errors)
