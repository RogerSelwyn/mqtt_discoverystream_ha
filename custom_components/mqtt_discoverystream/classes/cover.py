"""cover methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.cover import (
    ATTR_CURRENT_POSITION,
    ATTR_CURRENT_TILT_POSITION,
    ATTR_POSITION
)
from homeassistant.components.mqtt.cover import (
    CONF_GET_POSITION_TEMPLATE,
    CONF_GET_POSITION_TOPIC,
    CONF_TILT_STATUS_TEMPLATE,
    CONF_TILT_STATUS_TOPIC,
    DEFAULT_PAYLOAD_CLOSE,
    DEFAULT_PAYLOAD_OPEN,
    DEFAULT_PAYLOAD_STOP,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_CLOSE_COVER,
    SERVICE_OPEN_COVER,
    SERVICE_STOP_COVER,
    SERVICE_SET_COVER_POSITION,
    Platform,
)

from ..const import (
    ATTR_ATTRIBUTES,
    ATTR_SET,
    CONF_CMD_T,
)
from ..utils import EntityInfo, explode_message
from .entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Cover class."""

    PLATFORM = Platform.COVER

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a cover."""
        config[CONF_CMD_T] = f"{entity_info.mycommand}{ATTR_SET}"

        if ATTR_CURRENT_POSITION in entity_info.attributes:
            config[CONF_GET_POSITION_TOPIC] = f"{entity_info.mybase}{ATTR_ATTRIBUTES}"
            config[CONF_GET_POSITION_TEMPLATE] = (
                "{{ value_json['" + ATTR_CURRENT_POSITION + "'] }}"
            )
        if ATTR_CURRENT_TILT_POSITION in entity_info.attributes:
            config[CONF_TILT_STATUS_TOPIC] = f"{entity_info.mybase}{ATTR_ATTRIBUTES}"
            config[CONF_TILT_STATUS_TEMPLATE] = (
                "{{ value_json['" + ATTR_CURRENT_TILT_POSITION + "'] }}"
            )

    async def _async_handle_message(self, msg):
        """Handle a message for a cover."""
        domain, entity, element = explode_message(self._hass, msg)  # pylint: disable=unused-variable
        if not domain:
            return

        if msg.payload == DEFAULT_PAYLOAD_OPEN:
            await self._hass.services.async_call(
                domain, SERVICE_OPEN_COVER, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        elif msg.payload == DEFAULT_PAYLOAD_CLOSE:
            await self._hass.services.async_call(
                domain, SERVICE_CLOSE_COVER, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        elif msg.payload == DEFAULT_PAYLOAD_STOP:
            await self._hass.services.async_call(
                domain, SERVICE_STOP_COVER, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        elif msg.payload.isdigit() and int(msg.payload) >= 0:
            await self._hass.services.async_call(
                domain, SERVICE_SET_COVER_POSITION, {ATTR_ENTITY_ID: f"{domain}.{entity}", ATTR_POSITION: msg.payload}
            )
        else:
            _LOGGER.error(
                'Invalid service for "%s" - payload: %s for %s',
                ATTR_SET,
                {msg.payload},
                {entity},
            )
