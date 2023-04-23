"""cover methods for MQTT Discovery Statestream."""
import logging

from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_CLOSE_COVER,
    SERVICE_OPEN_COVER,
    STATE_CLOSED,
    STATE_OPEN,
    Platform,
)

from ..const import ATTR_SET, CONF_CMD_T, CONF_PL_CLOSED, CONF_PL_OPEN

_LOGGER = logging.getLogger(__name__)


class Cover:
    """Cover class."""

    def __init__(self, hass):
        """Initialise the cover class."""
        self._hass = hass

    def build_config(self, config, mycommand):
        """Build the config for a cover."""
        config[CONF_PL_CLOSED] = STATE_CLOSED
        config[CONF_PL_OPEN] = STATE_OPEN
        config[CONF_CMD_T] = f"{mycommand}{ATTR_SET}"

    async def async_subscribe(self, command_topic):
        """Subscribe to messages for a cover."""
        await self._hass.components.mqtt.async_subscribe(
            f"{command_topic}{Platform.COVER}/+/{ATTR_SET}",
            self._async_handle_message,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a cover."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]

        _LOGGER.debug(
            "Message received: topic %s; payload: %s", {msg.topic}, {msg.payload}
        )

        if msg.payload == STATE_OPEN:
            await self._hass.services.async_call(
                domain, SERVICE_OPEN_COVER, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        elif msg.payload == STATE_CLOSED:
            await self._hass.services.async_call(
                domain, SERVICE_CLOSE_COVER, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        else:
            _LOGGER.error(
                'Invalid service for "%s" - payload: %s for %s',
                ATTR_SET,
                {msg.payload},
                {entity},
            )
