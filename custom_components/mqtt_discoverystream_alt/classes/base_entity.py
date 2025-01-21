"""Base for all discovery entities."""

import json
import logging

from homeassistant.components import mqtt
from homeassistant.const import (
    ATTR_STATE,
)
from homeassistant.helpers.json import JSONEncoder

from ..const import (
    ATTR_ATTRIBUTES,
    SUPPORTED_ENTITY_TYPE_COMMANDS,
)
from ..utils import EntityInfo

_LOGGER = logging.getLogger(__name__)


class DiscoveryEntity:
    """Base discovery entity class."""

    PUBLISH_STATE = True

    def __init__(self, hass, publish_retain, platform, publish_state):
        """Initialise the base class."""
        self._hass = hass
        self._publish_retain = publish_retain
        self._publish_state = publish_state
        self._platform = platform
        self._commands = SUPPORTED_ENTITY_TYPE_COMMANDS[self._platform]

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a discovery entity."""

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a discovery entity."""

        await self._async_publish_base_attributes(
            new_state,
            mybase,
        )

    async def async_subscribe_commands(self, command_topic):
        """Subscribe to messages for an entity."""
        if not self._commands:
            return

        for command in self._commands:
            await mqtt.async_subscribe(
                self._hass,
                f"{command_topic}{self._platform}/+/{command}",
                self._async_handle_message,
            )

        _LOGGER.info("MQTT '%s' subscribe successful", self._platform)

    async def _async_handle_message(self, msg):
        """Handle a message for a discovery entity."""

    async def _async_publish_base_attributes(self, new_state, mybase):
        """Publish the basic attributes for the entity state."""
        if self._publish_state:
            await self._async_mqtt_publish(ATTR_STATE, new_state.state, mybase)

        attributes = dict(new_state.attributes.items())
        await self._async_mqtt_publish(
            ATTR_ATTRIBUTES, attributes, mybase, encoded=True
        )

    async def _async_mqtt_publish(self, topic, value, mybase, encoded=False):
        if encoded:
            value = json.dumps(value, cls=JSONEncoder)
        await mqtt.async_publish(
            self._hass,
            f"{mybase}{topic}",
            value,
            1,
            self._publish_retain,
        )

    async def async_publish_attribute_if_exists(
        self, new_state, mybase, attribute_name, strip=False
    ):
        """Publish a specific attribute"""
        if attribute_name in new_state.attributes:
            value = new_state.attributes[attribute_name]
            if value and strip:
                value = value.strip('"')
            await self._async_mqtt_publish(attribute_name, value, mybase)
