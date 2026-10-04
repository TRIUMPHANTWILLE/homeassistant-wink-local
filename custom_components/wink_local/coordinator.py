from __future__ import annotations

from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .device_mapper import WinkDeviceMapper
from .transport.aau import WinkAAUError, WinkAAUTokenExpired

class WinkCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api, interval: int) -> None:
        super().__init__(hass, logger=__import__("logging").getLogger(__name__), name="Wink Local", update_interval=timedelta(seconds=interval))
        self.api=api
        self.mapper=WinkDeviceMapper()
    async def _async_update_data(self):
        try:
            return self.mapper.map_devices(await self.api.async_get_devices())
        except WinkAAUTokenExpired as err:
            raise UpdateFailed("Wink local-control token expired") from err
        except WinkAAUError as err:
            raise UpdateFailed(str(err)) from err
