"""Image methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components import mqtt
from homeassistant.components.mqtt.image import CONF_URL_TOPIC
from homeassistant.const import ATTR_ENTITY_PICTURE, ATTR_STATE, Platform
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.network import get_url

from ..const import ATTR_ATTRIBUTES, CONF_ENT_PIC
from ..utils import EntityInfo, build_topic
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Image class."""

    PLATFORM = Platform.IMAGE

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a image."""

        if CONF_ENT_PIC in config:
            del config[CONF_ENT_PIC]
        config[CONF_URL_TOPIC] = build_topic(ATTR_ENTITY_PICTURE)

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a image."""
        if self._publish_state:
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{ATTR_STATE}",
                new_state.state,
                1,
                self._publish_retain,
            )

        attributes = dict(new_state.attributes.items())
        if ATTR_ENTITY_PICTURE in attributes:
            picture = attributes[ATTR_ENTITY_PICTURE]
            if picture.startswith(f"/api/image_proxy/{new_state.entity_id}"):
                url = get_url(self._hass, prefer_external=True)
                picture = url + picture
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{ATTR_ENTITY_PICTURE}",
                picture,
                1,
                self._publish_retain,
            )
            del attributes[ATTR_ENTITY_PICTURE]
            del attributes["access_token"]
        encoded = json.dumps(attributes, cls=JSONEncoder)
        await mqtt.async_publish(
            self._hass, f"{mybase}{ATTR_ATTRIBUTES}", encoded, 1, self._publish_retain
        )
