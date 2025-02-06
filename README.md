# Virtual Thermostat

A custom Home Assistant integration to create a virtual thermostat that adjusts the temperature of an external thermostat based on an external sensor and a configurable offset.

## Installation
1. Add this repository to HACS.
2. Install the integration.
3. Restart Home Assistant.
4. Configure via Configuration > Integrations.

## Configuration
- **Sensor**: The external temperature sensor (e.g., `sensor.living_room_temperature`).
- **Thermostat**: The external thermostat to control (e.g., `climate.living_room_thermostat`).
- **Offset**: The temperature difference between the sensor and the desired temperature (e.g., `2` for +2°C).

## Example
- **Sensor**: `sensor.living_room_temperature` (reads 20°C)
- **Thermostat**: `climate.living_room_thermostat`
- **Offset**: `2` (target temperature = 20°C + 2°C = 22°C)

The virtual thermostat will set the external thermostat to **22°C**.