"""sensor methods for MQTT Discovery Statestream."""

from homeassistant.components.mqtt.const import CONF_SUGGESTED_DISPLAY_PRECISION
from homeassistant.components.sensor import CONF_STATE_CLASS
from homeassistant.components.sensor import DOMAIN as sensordomain
from homeassistant.const import Platform
from homeassistant.helpers import entity_registry

from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, simple_attribute_add


class DiscoveryItem(DiscoveryEntity):
    """Sensor class."""

    PLATFORM = Platform.SENSOR

    def __init__(
        self,
        hass,
        base_topic,
        command_topic,
        publish_retain,
        discovered_entities,
        platform,
        publish_state,
    ):
        """Initialise the sensor class."""
        super().__init__(
            hass,
            base_topic,
            command_topic,
            publish_retain,
            discovered_entities,
            platform,
            publish_state,
        )
        self._ent_reg = entity_registry.async_get(hass)

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a sensor."""

        entry = self._ent_reg.async_get(entity_info.entity_id)
        simple_attribute_add(config, entity_info.attributes, CONF_STATE_CLASS)
        if entry and (options := entry.options) and sensordomain in options:
            sensor_options = options[sensordomain]
            if CONF_SUGGESTED_DISPLAY_PRECISION in sensor_options:
                config[CONF_SUGGESTED_DISPLAY_PRECISION] = sensor_options[
                    CONF_SUGGESTED_DISPLAY_PRECISION
                ]
