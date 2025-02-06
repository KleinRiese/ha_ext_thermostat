from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "ext_thermostat"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Füge die Entität zu Home Assistant hinzu
    hass.data.setdefault(DOMAIN, {})
    
    # Registriere die Entität für die climate-Plattform
    await hass.config_entries.async_forward_entry_setup(entry, "climate")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Entferne die Entität
    await hass.config_entries.async_forward_entry_unload(entry, "climate")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True