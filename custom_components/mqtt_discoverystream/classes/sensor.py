"""sensor methods for MQTT Discovery Statestream."""

from homeassistant.components.sensor import DOMAIN as sensordomain
from homeassistant.helpers import entity_registry

from ..const import ATTR_SUGGESTED_DISPLAY_PRECISION, CONF_SUG_DSP_PRC


class Sensor:
    """Sensor class."""

    def __init__(self, hass):
        """Initialise the sensor class."""
        self._ent_reg = entity_registry.async_get(hass)
        self._hass = hass

    def build_config(self, config, mycommand, attributes, mybase, entity_id, *args):  # pylint: disable=unused-argument
        """Build the config for a sensor."""

        if entry := self._ent_reg.async_get(entity_id):
            if options := entry.options:
                if sensordomain in options:
                    sensor_options = options[sensordomain]
                    if ATTR_SUGGESTED_DISPLAY_PRECISION in sensor_options:
                        config[CONF_SUG_DSP_PRC] = sensor_options[
                            ATTR_SUGGESTED_DISPLAY_PRECISION
                        ]
