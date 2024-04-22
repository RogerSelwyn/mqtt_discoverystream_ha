"""number methods for MQTT Discovery Statestream."""

from homeassistant.components.number import (
    ATTR_MAX,
    ATTR_MIN,
    ATTR_STEP,
    ATTR_VALUE,
    SERVICE_SET_VALUE,
)
from homeassistant.const import ATTR_ENTITY_ID, Platform

from ..const import (
    ATTR_MODE,
    ATTR_SET,
    CONF_CMD_T,
    CONF_MAX,
    CONF_MIN,
    CONF_MODE,
    CONF_STEP,
)
from ..utils import EntityInfo, validate_message
from .entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Number class."""

    PLATFORM = Platform.NUMBER

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a number."""
        config[CONF_CMD_T] = f"{entity_info.mycommand}{ATTR_SET}"
        config[CONF_MAX] = entity_info.attributes[ATTR_MAX]
        config[CONF_MIN] = entity_info.attributes[ATTR_MIN]
        config[CONF_MODE] = entity_info.attributes[ATTR_MODE]
        config[CONF_STEP] = entity_info.attributes[ATTR_STEP]

    async def _async_handle_message(self, msg):
        """Handle a message for a number."""
        valid, domain, entity, command = validate_message(  # pylint: disable=unused-variable
            self._hass, msg, DiscoveryItem.PLATFORM
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_VALUE: msg.payload,
        }
        await self._hass.services.async_call(domain, SERVICE_SET_VALUE, service_payload)
