"""binary_sensor methods for MQTT Discovery Statestream."""

from homeassistant.const import STATE_OFF, STATE_ON


class BinarySensor:
    """Binary_sensor class."""

    def build_config(self, config, *args):  # pylint: disable=unused-argument
        """Build the config for a binary_sensor."""
        config["pl_off"] = STATE_OFF
        config["pl_on"] = STATE_ON
