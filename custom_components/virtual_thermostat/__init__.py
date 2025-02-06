from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .climate import VirtualThermostat

DOMAIN = "virtual_thermostat"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Erstelle die Entität
    thermostat = VirtualThermostat(hass, entry.data)
    
    # Füge die Entität zu Home Assistant hinzu
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = thermostat
    
    # Registriere die Entität für die climate-Plattform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "climate")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Entferne die Entität
    await hass.config_entries.async_forward_entry_unload(entry, "climate")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True