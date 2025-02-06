import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVAC_MODE_HEAT, SUPPORT_TARGET_TEMPERATURE
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

class VirtualThermostat(ClimateEntity):
    def __init__(self, hass, name, sensor_entity_id, thermostat_entity_id):
        self.hass = hass
        self._name = name
        self._sensor_entity_id = sensor_entity_id
        self._thermostat_entity_id = thermostat_entity_id
        self._target_temperature = 20.0  # Standard-Sollwert
        self._current_temperature = None
        self._thermostat_temperature = None
        
    @property
    def name(self):
        return self._name
    
    @property
    def temperature_unit(self):
        return TEMP_CELSIUS
    
    @property
    def current_temperature(self):
        return self._current_temperature
    
    @property
    def target_temperature(self):
        return self._target_temperature
    
    @property
    def hvac_mode(self):
        return HVAC_MODE_HEAT
    
    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE
    
    def set_temperature(self, **kwargs):
        if ATTR_TEMPERATURE in kwargs:
            self._target_temperature = kwargs[ATTR_TEMPERATURE]
            self._update_real_thermostat()
            self.schedule_update_ha_state()
    
    @callback
    def async_update(self):
        sensor_state = self.hass.states.get(self._sensor_entity_id)
        thermostat_state = self.hass.states.get(self._thermostat_entity_id)
        
        if sensor_state and sensor_state.state not in [None, "unknown", "unavailable"]:
            self._current_temperature = float(sensor_state.state)
        
        if thermostat_state and thermostat_state.state not in [None, "unknown", "unavailable"]:
            self._thermostat_temperature = float(thermostat_state.state)
        
        self._update_real_thermostat()
    
    def _update_real_thermostat(self):
        if self._current_temperature is not None and self._thermostat_temperature is not None:
            offset = self._current_temperature - self._thermostat_temperature
            real_target = self._target_temperature + offset
            self.hass.services.call(
                "climate", "set_temperature", 
                {"entity_id": self._thermostat_entity_id, "temperature": real_target}
            )
        _LOGGER.debug("Updated real thermostat: %s", self._thermostat_entity_id)
