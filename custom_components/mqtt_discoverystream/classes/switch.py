"""switch methods for MQTT Discovery Statestream."""

from homeassistant.const import STATE_OFF, STATE_ON


class Switch:
    """Switch class."""

    def build_config(self, config, mybase):
        """Build the config for a switch."""
        config["pl_off"] = STATE_OFF
        config["pl_on"] = STATE_ON
        config["cmd_t"] = f"{mybase}set"
