from __future__ import annotations
import voluptuous as vol
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import config_validation as cv
from .const import *
from .transport.aau import WinkAAUClient
from .transport.ssh import WinkSSHClient
from .coordinator import WinkCoordinator
from .device_mapper import WinkDeviceMapper
async def async_setup_entry(hass,entry):
    api=WinkAAUClient(async_get_clientsession(hass),entry.data[CONF_HOST],entry.data.get(CONF_PORT,DEFAULT_PORT),entry.data[CONF_TOKEN],entry.data.get(CONF_VERIFY_SSL,False))
    coordinator=WinkCoordinator(hass,api,entry.data.get(CONF_SCAN_INTERVAL,DEFAULT_SCAN_INTERVAL)); coordinator.api=api; await coordinator.async_config_entry_first_refresh()
    ssh=None
    if entry.data.get(CONF_SSH_ENABLED): ssh=WinkSSHClient(entry.data[CONF_HOST],entry.data.get(CONF_SSH_PORT,22),entry.data.get(CONF_SSH_USER,"root"),entry.data.get(CONF_SSH_PASSWORD),entry.data.get(CONF_SSH_PRIVATE_KEY))
    hass.data.setdefault(DOMAIN,{})[entry.entry_id]={"api":api,"ssh":ssh,"coordinator":coordinator,"mapper":WinkDeviceMapper()}
    await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS)
    await _register_services(hass)
    return True
async def async_unload_entry(hass,entry):
    ok=await hass.config_entries.async_unload_platforms(entry,PLATFORMS)
    if ok: hass.data[DOMAIN].pop(entry.entry_id,None)
    return ok
async def _register_services(hass):
    if hass.services.has_service(DOMAIN,"start_pairing"): return
    def first():
        if not hass.data.get(DOMAIN): raise ValueError("No Wink Local entry")
        return next(iter(hass.data[DOMAIN].values()))
    async def pairing(call):
        data=first(); ssh=data["ssh"]
        if not ssh: raise ValueError("SSH management is not configured")
        await ssh.start_pairing(call.data[ATTR_RADIO],call.data.get(ATTR_TIMEOUT,60)); await data["coordinator"].async_request_refresh()
    async def exclusion(call):
        data=first(); ssh=data["ssh"]
        if not ssh: raise ValueError("SSH management is not configured")
        await ssh.start_exclusion(call.data.get(ATTR_TIMEOUT,60)); await data["coordinator"].async_request_refresh()
    async def device_cmd(call,method):
        data=first(); ssh=data["ssh"]
        if not ssh: raise ValueError("SSH management is not configured")
        await getattr(ssh,method)(call.data[ATTR_MASTER_ID]); await data["coordinator"].async_request_refresh()
    hass.services.async_register(DOMAIN,"start_pairing",pairing,schema=vol.Schema({vol.Required(ATTR_RADIO):vol.In(SUPPORTED_RADIOS),vol.Optional(ATTR_TIMEOUT,default=60):cv.positive_int}))
    hass.services.async_register(DOMAIN,"start_exclusion",exclusion,schema=vol.Schema({vol.Optional(ATTR_TIMEOUT,default=60):cv.positive_int}))
    hass.services.async_register(DOMAIN,"refresh_device",lambda c: device_cmd(c,"refresh"),schema=vol.Schema({vol.Required(ATTR_MASTER_ID):cv.positive_int}))
    hass.services.async_register(DOMAIN,"reconfigure_device",lambda c: device_cmd(c,"reconfigure"),schema=vol.Schema({vol.Required(ATTR_MASTER_ID):cv.positive_int}))
    async def remove(call):
        data=first(); ssh=data["ssh"]
        if not ssh: raise ValueError("SSH management is not configured")
        await ssh.remove(call.data[ATTR_MASTER_ID],call.data.get(ATTR_FORCE,False)); await data["coordinator"].async_request_refresh()
    async def rename(call):
        data=first(); ssh=data["ssh"]
        if not ssh: raise ValueError("SSH management is not configured")
        await ssh.rename(call.data[ATTR_MASTER_ID],call.data[ATTR_NAME]); await data["coordinator"].async_request_refresh()
    async def scene(call): await first()["api"].async_run_scene(call.data[ATTR_SCENE])
    hass.services.async_register(DOMAIN,"remove_device",remove,schema=vol.Schema({vol.Required(ATTR_MASTER_ID):cv.positive_int,vol.Optional(ATTR_FORCE,default=False):bool}))
    hass.services.async_register(DOMAIN,"rename_device",rename,schema=vol.Schema({vol.Required(ATTR_MASTER_ID):cv.positive_int,vol.Required(ATTR_NAME):cv.string}))
    hass.services.async_register(DOMAIN,"run_scene",scene,schema=vol.Schema({vol.Required(ATTR_SCENE):list}))
