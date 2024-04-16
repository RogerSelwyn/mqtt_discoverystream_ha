"""input_select methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components import mqtt
from homeassistant.components.input_select import DOMAIN as IS_DOMAIN
from homeassistant.components.select import ATTR_OPTION, ATTR_OPTIONS
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_SELECT_OPTION,
)

from ..const import (
    ATTR_SET,
    CONF_CMD_T,
    CONF_OPS,
    CONF_PUBLISHED,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class InputSelect:
    """Input_Select class."""

    def __init__(self, hass):
        """Initialise the input_select class."""
        self._hass = hass

    def build_config(self, config, attributes, mycommand):
        """Build the config for a input_select."""
        if ATTR_OPTIONS in attributes:
            config[CONF_OPS] = attributes[ATTR_OPTIONS]
        config[CONF_CMD_T] = f"{mycommand}{ATTR_SET}"

    async def async_subscribe(self, command_topic):
        """Subscribe to messages for a input_select."""
        await mqtt.async_subscribe(
            self._hass,
            f"{command_topic}{IS_DOMAIN}/+/{ATTR_SET}",
            self._async_handle_message,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a input_select."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]

        # Only handle service calls for discoveries we published
        if f"{domain}.{entity}" not in self._hass.data[DOMAIN][CONF_PUBLISHED]:
            return

        _LOGGER.debug(
            "Message received: topic %s; payload: %s", {msg.topic}, {msg.payload}
        )

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_OPTION: msg.payload,
        }
        await self._hass.services.async_call(
            domain, SERVICE_SELECT_OPTION, service_payload
        )
