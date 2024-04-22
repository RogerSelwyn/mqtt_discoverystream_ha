"""event methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components import mqtt
from homeassistant.components.event import ATTR_EVENT_TYPE, ATTR_EVENT_TYPES
from homeassistant.const import ATTR_STATE, Platform
from homeassistant.helpers.json import JSONEncoder

from ..const import (
    CONF_EVT_TYP,
)
from ..utils import EntityInfo
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Event class."""

    PLATFORM = Platform.EVENT

    def __init__(
        self,
        hass,
        publish_retain,
        platform,
    ):
        """Initialise the text class."""
        super().__init__(
            hass,
            publish_retain,
            platform,
            publish_state=False,
        )

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a event."""
        config[CONF_EVT_TYP] = entity_info.attributes[ATTR_EVENT_TYPES]

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a text."""

        payload = json.dumps(
            {ATTR_EVENT_TYPE: new_state.attributes[ATTR_EVENT_TYPE]}, cls=JSONEncoder
        )
        await mqtt.async_publish(
            self._hass,
            f"{mybase}{ATTR_STATE}",
            payload,
            1,
            self._publish_retain,
        )

        await super().async_publish_state(new_state, mybase)
