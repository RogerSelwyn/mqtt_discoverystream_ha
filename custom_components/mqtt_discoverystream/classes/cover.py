"""cover methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components import mqtt
from homeassistant.components.cover import (
    ATTR_CURRENT_POSITION,
    ATTR_CURRENT_TILT_POSITION,
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
    ATTR_STATE,
    SERVICE_CLOSE_COVER,
    SERVICE_OPEN_COVER,
    SERVICE_STOP_COVER,
    Platform,
)

from ..const import (
    ATTR_ATTRIBUTES,
    ATTR_SET,
    CONF_CMD_T,
    CONF_PUBLISHED,
    DOMAIN,
)
from ..utils import EntityInfo
from .entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class Cover(DiscoveryEntity):
    """Cover class."""

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

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a light."""
        await super().async_publish_state(new_state, mybase)

        await mqtt.async_publish(
            self._hass,
            f"{mybase}{ATTR_STATE}",
            new_state.state,
            1,
            self._publish_retain,
        )

    async def async_subscribe(self, command_topic):
        """Subscribe to messages for a cover."""
        await mqtt.async_subscribe(
            self._hass,
            f"{command_topic}{Platform.COVER}/+/{ATTR_SET}",
            self._async_handle_message,
        )
        return True

    async def _async_handle_message(self, msg):
        """Handle a message for a cover."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]

        # Only handle service calls for discoveries we published
        if f"{domain}.{entity}" not in self._hass.data[DOMAIN][CONF_PUBLISHED]:
            return

        _LOGGER.debug(
            "Message received: topic %s; payload: %s", {msg.topic}, {msg.payload}
        )

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
        else:
            _LOGGER.error(
                'Invalid service for "%s" - payload: %s for %s',
                ATTR_SET,
                {msg.payload},
                {entity},
            )
