from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.helpers.restore_state import RestoreEntity

class VirtualThermostat(ClimateEntity, RestoreEntity):
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]

    def __init__(self, hass, config):
        self._hass = hass
        self._sensor = config[CONF_SENSOR]
        self._thermostat = config[CONF_THERMOSTAT]
        self._offset = config[CONF_OFFSET]
        self._target_temperature = None

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self._hass.helpers.event.async_track_state_change(
                self._sensor, self._async_sensor_updated
            )
        )

    async def _async_sensor_updated(self, entity_id, old_state, new_state):
        if new_state is None:
            return
        sensor_temp = float(new_state.state)
        calculated_temp = sensor_temp + self._offset
        self._target_temperature = calculated_temp
        await self._hass.services.async_call(
            "climate",
            "set_temperature",
            {"entity_id": self._thermostat, "temperature": calculated_temp},
        )
        self.async_write_ha_state()

    @property
    def current_temperature(self):
        return self._hass.states.get(self._sensor).state

    @property
    def target_temperature(self):
        return self._target_temperature

    async def async_set_temperature(self, **kwargs):
        self._target_temperature = kwargs.get(ATTR_TEMPERATURE)
        self.async_write_ha_state()