"""switch methods for MQTT Discovery Statestream."""

from homeassistant.const import STATE_OFF, STATE_ON

from ..const import ATTR_SET, CONF_CMD_T, CONF_PL_OFF, CONF_PL_ON


class Switch:
    """Switch class."""

    def build_config(self, config, mybase):
        """Build the config for a switch."""
        config[CONF_PL_OFF] = STATE_OFF
        config[CONF_PL_ON] = STATE_ON
        config[CONF_CMD_T] = f"{mybase}{ATTR_SET}"
