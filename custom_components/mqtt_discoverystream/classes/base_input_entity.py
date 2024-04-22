"""Base for all discovery entities with input alternatives."""

import logging

from homeassistant.components.select import ATTR_OPTION, ATTR_OPTIONS
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_SELECT_OPTION,
    Platform,
)

from ..const import (
    ATTR_SET,
    CONF_CMD_T,
    CONF_OPS,
)
from ..utils import EntityInfo, validate_message
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class SelectDiscoveryEntity(DiscoveryEntity):
    """Select class."""

    PLATFORM = Platform.SELECT

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a select."""
        if ATTR_OPTIONS in entity_info.attributes:
            config[CONF_OPS] = entity_info.attributes[ATTR_OPTIONS]
        config[CONF_CMD_T] = f"{entity_info.mycommand}{ATTR_SET}"

    async def _async_handle_message(self, msg):
        """Handle a message for a select."""
        valid, domain, entity, command = validate_message(  # pylint: disable=unused-variable
            self._hass, msg, self._platform
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_OPTION: msg.payload,
        }
        await self._hass.services.async_call(
            domain, SERVICE_SELECT_OPTION, service_payload
        )
