"""Base for all discovery entities."""

import logging

from homeassistant.components import mqtt

from ..const import SUPPORTED_COMMANDS
from ..utils import EntityInfo, async_publish_base_attributes

_LOGGER = logging.getLogger(__name__)


class DiscoveryEntity:
    """Base discovery entity class."""

    def __init__(self, hass, publish_retain, platform, publish_state=True):
        """Initialise the climate class."""
        self._hass = hass
        self._publish_retain = publish_retain
        self._publish_state = publish_state
        self._platform = platform
        self._commands = SUPPORTED_COMMANDS[self._platform]

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a discovery entity."""

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a discovery entity."""

        await async_publish_base_attributes(
            self._hass,
            new_state,
            mybase,
            self._publish_retain,
            publish_state=self._publish_state,
        )

    async def async_subscribe(self, command_topic):
        """Subscribe to messages for a cover."""
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
