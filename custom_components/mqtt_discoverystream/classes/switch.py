"""switch methods for MQTT Discovery Statestream."""

import logging

from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)

from ..const import (
    ATTR_SET,
    CONF_CMD_T,
    CONF_PL_OFF,
    CONF_PL_ON,
)
from ..utils import EntityInfo, explode_message
from .entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class Switch(DiscoveryEntity):
    """Switch class."""

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a switch."""
        config[CONF_PL_OFF] = STATE_OFF
        config[CONF_PL_ON] = STATE_ON
        config[CONF_CMD_T] = f"{entity_info.mycommand}{ATTR_SET}"

    async def _async_handle_message(self, msg):
        """Handle a message for a switch."""
        domain, entity, element = explode_message(self._hass, msg)  # pylint: disable=unused-variable
        if not domain:
            return

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
