"""Base for all discovery entities."""

from ..utils import EntityInfo, async_publish_base_attributes


class DiscoveryEntity:
    """Base discovery entity class."""

    def __init__(self, hass, publish_retain, publish_state=True):
        """Initialise the climate class."""
        self._hass = hass
        self._publish_retain = publish_retain
        self._publish_state = publish_state

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

    async def async_subscribe(self, command_topic):  # pylint: disable=unused-argument
        """Subscribe to messages for discovery entity."""
        return False
