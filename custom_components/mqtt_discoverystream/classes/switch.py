"""switch methods for MQTT Discovery Statestream."""
import logging

from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)

from ..const import ATTR_SET, CONF_CMD_T, CONF_PL_OFF, CONF_PL_ON

_LOGGER = logging.getLogger(__name__)


class Switch:
    """Switch class."""

    def __init__(self, hass, base_topic):
        """Initialise the switch class."""
        self._hass = hass
        self._base_topic = base_topic

    def build_config(self, config, mybase):
        """Build the config for a switch."""
        config[CONF_PL_OFF] = STATE_OFF
        config[CONF_PL_ON] = STATE_ON
        config[CONF_CMD_T] = f"{mybase}{ATTR_SET}"

    async def async_subscribe(self):
        """Subscribe to messages for a switch."""
        await self._hass.components.mqtt.async_subscribe(
            f"{self._base_topic}{Platform.SWITCH}/+/{ATTR_SET}",
            self._async_handle_message,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a switch."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]

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
