"""Discovery for MQTT Discovery Stream."""
import logging

from homeassistant.components import mqtt
from homeassistant.components.mqtt import DOMAIN as MQTT_DOMAIN
from homeassistant.components.mqtt.const import (
    CONF_AVAILABILITY,
    DEFAULT_PAYLOAD_AVAILABLE,
    DEFAULT_PAYLOAD_NOT_AVAILABLE,
)
from homeassistant.const import CONF_INCLUDE, STATE_UNAVAILABLE, STATE_UNKNOWN, Platform
from homeassistant.setup import async_when_setup

from .classes.climate import Climate
from .classes.cover import Cover
from .classes.light import Light
from .classes.switch import Switch
from .const import (
    CONF_BASE_TOPIC,
    CONF_COMMAND_TOPIC,
    CONF_DISCOVERY_TOPIC,
    CONF_PUBLISHED,
    DOMAIN,
)
from .discovery import Discovery
from .utils import async_publish_base_attributes

_LOGGER = logging.getLogger(__name__)


class Publisher:
    """Manage publication for MQTT Discovery Statestream."""

    def __init__(self, hass, conf):
        """Initiate publishing."""
        self._hass = hass
        self._has_includes = bool(conf.get(CONF_INCLUDE))
        self._discovery_topic = conf.get(CONF_DISCOVERY_TOPIC) or conf.get(
            CONF_BASE_TOPIC
        )
        self._command_topic = conf.get(CONF_COMMAND_TOPIC) or conf.get(CONF_BASE_TOPIC)
        if not self._command_topic.endswith("/"):
            self._command_topic = f"{self._command_topic}/"
        self._hass.data[DOMAIN] = {CONF_PUBLISHED: []}
        self._climate = Climate(hass)
        self._light = Light(hass)
        self._switch = Switch(hass)
        self._cover = Cover(hass)
        self._discovery = Discovery(hass, conf)
        async_when_setup(hass, MQTT_DOMAIN, self._async_subscribe)

    async def async_state_publish(self, entity_id, new_state, mybase):
        """Publish state for MQTT Discovery Statestream."""
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if entity_id not in self._hass.data[DOMAIN][CONF_PUBLISHED]:
            await self._discovery.async_discovery_publish(
                entity_id, new_state.attributes, mybase
            )

        if ent_domain == Platform.LIGHT:
            await self._light.async_publish_state(new_state, mybase)
        elif ent_domain == Platform.CLIMATE:
            await self._climate.async_publish_state(new_state, mybase)
        elif ent_domain == Platform.COVER:
            await self._cover.async_publish_state(new_state, mybase)
        else:
            await async_publish_base_attributes(self._hass, new_state, mybase)

        payload = (
            DEFAULT_PAYLOAD_NOT_AVAILABLE
            if new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, None)
            else DEFAULT_PAYLOAD_AVAILABLE
        )
        await mqtt.async_publish(
            self._hass, f"{mybase}{CONF_AVAILABILITY}", payload, 1, True
        )

    async def _async_subscribe(
        self, hass, component
    ):  # pylint: disable=unused-argument
        """Subscribe to neccesary topics as part MQTT Discovery Statestream."""
        await self._climate.async_subscribe(self._command_topic)
        await self._light.async_subscribe(self._command_topic)
        await self._switch.async_subscribe(self._command_topic)
        await self._cover.async_subscribe(self._command_topic)
        _LOGGER.info("MQTT subscribe successful")
