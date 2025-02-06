from homeassistant.components.climate import ClimateEntity, HVACMode
from homeassistant.components.climate.const import ClimateEntityFeature
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the climate platform for the virtual thermostat."""
    # Erstelle die Entität
    thermostat = VirtualThermostat(hass, entry.data)
    
    # Füge die Entität hinzu
    async_add_entities([thermostat])

class VirtualThermostat(ClimateEntity, RestoreEntity):
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_hvac_mode = HVACMode.HEAT  # Standardmodus: Heizen

    def __init__(self, hass, config):
        self._hass = hass
        self._sensor = config["sensor"]
        self._thermostat = config["thermostat"]
        self._target_temperature = None
        self._current_temperature = None

    @property
    def name(self):
        return "Virtual Thermostat"

    @property
    def unique_id(self):
        return f"virtual_thermostat_{self._sensor}_{self._thermostat}"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        
        # Wiederherstellen des vorherigen Zustands
        state = await self.async_get_last_state()
        if state:
            self._target_temperature = state.attributes.get("temperature")
            self._attr_hvac_mode = state.attributes.get("hvac_mode", HVACMode.HEAT)
        
        # Überwache den Sensor
        self.async_on_remove(
            self._hass.helpers.event.async_track_state_change(
                self._sensor, self._async_sensor_updated
            )
        )

    async def _async_sensor_updated(self, entity_id, old_state, new_state):
        if new_state is None:
            return
        self._current_temperature = float(new_state.state)
        await self._update_thermostat()

    async def _update_thermostat(self):
        if self._target_temperature is None or self._current_temperature is None:
            return

        # Setze die Zieltemperatur am externen Thermostaten
        await self._hass.services.async_call(
            "climate",
            "set_temperature",
            {"entity_id": self._thermostat, "temperature": self._target_temperature},
        )
        self.async_write_ha_state()

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    async def async_set_temperature(self, **kwargs):
        self._target_temperature = kwargs.get(ATTR_TEMPERATURE)
        await self._update_thermostat()
        self.async_write_ha_state()