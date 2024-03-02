"""switch methods for MQTT Discovery Statestream."""
import logging

from homeassistant.components import mqtt
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)

from ..const import (
    ATTR_SET,
    CONF_CMD_T,
    CONF_PL_OFF,
    CONF_PL_ON,
    CONF_PUBLISHED,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class Switch:
    """Switch class."""

    def __init__(self, hass):
        """Initialise the switch class."""
        self._hass = hass

    def build_config(self, config, mycommand):
        """Build the config for a switch."""
        config[CONF_PL_OFF] = STATE_OFF
        config[CONF_PL_ON] = STATE_ON
        config[CONF_CMD_T] = f"{mycommand}{ATTR_SET}"

    async def async_subscribe(self, command_topic):
        """Subscribe to messages for a switch."""
        await mqtt.async_subscribe(
            self._hass,
            f"{command_topic}{Platform.SWITCH}/+/{ATTR_SET}",
            self._async_handle_message,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a switch."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]

        # Only handle service calls for discoveries we published
        if f"{domain}.{entity}" not in self._hass.data[DOMAIN][CONF_PUBLISHED]:
            return

        _LOGGER.debug(
            "Message received: topic %s; payload: %s", {msg.topic}, {msg.payload}
        )

        if msg.payload == STATE_ON:
            await self._hass.services.async_call(
                domain, SERVICE_TURN_ON, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        elif msg.payload == STATE_OFF:
            await self._hass.services.async_call(
                domain, SERVICE_TURN_OFF, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        else:
            _LOGGER.error(
                'Invalid service for "%s" - payload: %s for %s',
                ATTR_SET,
                {msg.payload},
                {entity},
            )
