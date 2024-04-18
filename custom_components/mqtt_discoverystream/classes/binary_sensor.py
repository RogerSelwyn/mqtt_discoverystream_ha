"""binary_sensor methods for MQTT Discovery Statestream."""

from homeassistant.const import STATE_OFF, STATE_ON

from ..utils import EntityInfo
from .entity import DiscoveryEntity


class BinarySensor(DiscoveryEntity):
    """Binary_sensor class."""

    def build_config(self, config, entity_info: EntityInfo):  # pylint: disable=unused-argument
        """Build the config for a binary_sensor."""
        config["pl_off"] = STATE_OFF
        config["pl_on"] = STATE_ON
