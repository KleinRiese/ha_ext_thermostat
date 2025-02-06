from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .climate import VirtualThermostat

DOMAIN = "virtual_thermostat"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    config = entry.data
    thermostat = VirtualThermostat(hass, config)
    hass.data[DOMAIN][entry.entry_id] = thermostat
    await hass.config_entries.async_forward_entry_setup(entry, "climate")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "climate")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True