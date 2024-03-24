"""Discovery for MQTT Discovery Stream."""
import asyncio
import logging

from homeassistant.components import mqtt
from homeassistant.components.mqtt import DOMAIN as MQTT_DOMAIN
from homeassistant.components.mqtt.const import (
    CONF_AVAILABILITY,
    DEFAULT_PAYLOAD_AVAILABLE,
    DEFAULT_PAYLOAD_NOT_AVAILABLE,
)
from homeassistant.const import (
    CONF_INCLUDE,
    EVENT_HOMEASSISTANT_STARTED,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    Platform,
)
from homeassistant.helpers import entity_registry
from homeassistant.helpers.entityfilter import convert_include_exclude_filter
from homeassistant.helpers.event import async_call_later
from homeassistant.setup import async_when_setup

from .classes.climate import Climate
from .classes.cover import Cover
from .classes.light import Light
from .classes.switch import Switch
from .const import (
    CONF_BASE_TOPIC,
    CONF_BIRTH_TOPIC,
    CONF_COMMAND_TOPIC,
    CONF_DISCOVERY_TOPIC,
    CONF_PUBLISHED,
    CONF_REPUBLISH_TIME,
    DEFAULT_STATE_SLEEP,
    DOMAIN,
)
from .discovery import Discovery
from .utils import async_publish_base_attributes

_LOGGER = logging.getLogger(__name__)


class Publisher:
    """Manage publication for MQTT Discovery Statestream."""

    def __init__(self, hass, conf, base_topic, publish_retain):
        """Initiate publishing."""
        self._hass = hass
        self._base_topic = base_topic
        self._publish_retain = publish_retain
        self._has_includes = bool(conf.get(CONF_INCLUDE))
        self._loop_time = conf.get(CONF_REPUBLISH_TIME)
        self._discovery_topic = conf.get(CONF_DISCOVERY_TOPIC) or conf.get(
            CONF_BASE_TOPIC
        )
        self._command_topic = conf.get(CONF_COMMAND_TOPIC) or conf.get(CONF_BASE_TOPIC)
        if not self._command_topic.endswith("/"):
            self._command_topic = f"{self._command_topic}/"
        self._birth_topic = conf.get(CONF_BIRTH_TOPIC) or conf.get(CONF_BASE_TOPIC)
        if not self._birth_topic.endswith("/status"):
            self._birth_topic = f"{self._birth_topic}/status"
        self._hass.data[DOMAIN] = {CONF_PUBLISHED: []}
        self._climate = Climate(hass, self._publish_retain)
        self._light = Light(hass, self._publish_retain)
        self._switch = Switch(hass)
        self._cover = Cover(hass, self._publish_retain)
        self._discovery = Discovery(hass, conf)
        self._publish_filter = convert_include_exclude_filter(conf)
        async_when_setup(hass, MQTT_DOMAIN, self._async_subscribe)
        self._register_services()
        self._listen_for_hass_started()

    async def async_state_publish(self, entity_id, new_state, mybase):
        """Publish state for MQTT Discovery Statestream."""
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if entity_id not in self._hass.data[DOMAIN][CONF_PUBLISHED]:
            await self._discovery.async_discovery_publish(
                entity_id, new_state.attributes, mybase
            )
            await asyncio.sleep(DEFAULT_STATE_SLEEP)

        if new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, None):
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{CONF_AVAILABILITY}",
                DEFAULT_PAYLOAD_NOT_AVAILABLE,
                1,
                self._publish_retain,
            )
            return

        if ent_domain == Platform.LIGHT:
            await self._light.async_publish_state(new_state, mybase)
        elif ent_domain == Platform.CLIMATE:
            await self._climate.async_publish_state(new_state, mybase)
        elif ent_domain == Platform.COVER:
            await self._cover.async_publish_state(new_state, mybase)
        else:
            await async_publish_base_attributes(
                self._hass, new_state, mybase, self._publish_retain
            )

        await mqtt.async_publish(
            self._hass,
            f"{mybase}{CONF_AVAILABILITY}",
            DEFAULT_PAYLOAD_AVAILABLE,
            1,
            self._publish_retain,
        )

    async def _async_subscribe(self, hass, component):  # pylint: disable=unused-argument
        """Subscribe to neccesary topics as part MQTT Discovery Statestream."""
        await self._climate.async_subscribe(self._command_topic)
        await self._light.async_subscribe(self._command_topic)
        await self._switch.async_subscribe(self._command_topic)
        await self._cover.async_subscribe(self._command_topic)
        await self._async_birth_subscribe()
        _LOGGER.info("MQTT subscribe successful")

    async def _async_birth_subscribe(self):
        """Subscribe birth messages."""
        await mqtt.async_subscribe(
            self._hass,
            f"{self._birth_topic}",
            self._async_handle_birth_message,
        )

    async def _async_handle_birth_message(self, msg):
        if msg.payload == "online":
            await self._async_publish_discovery_state()

    def _register_services(self):
        self._hass.services.async_register(
            DOMAIN, "publish_discovery_state", self._async_publish_discovery_state
        )

    async def _async_publish_discovery_state(self, call=None):  # pylint: disable=unused-argument
        ent_reg = entity_registry.async_get(self._hass)
        entity_states = {}
        for entity_id in list(ent_reg.entities):
            if self._publish_filter(entity_id):
                if current_state := self._hass.states.get(entity_id):
                    mybase = f"{self._base_topic}{entity_id.replace('.', '/')}/"
                    await self._discovery.async_discovery_publish(
                        entity_id, current_state.attributes, mybase
                    )
                    entity_states[entity_id] = current_state
        _LOGGER.info("Discovery published")
        await asyncio.sleep(DEFAULT_STATE_SLEEP)
        for entity_id, current_state in entity_states.items():
            mybase = f"{self._base_topic}{entity_id.replace('.', '/')}/"
            await self.async_state_publish(entity_id, current_state, mybase)
        _LOGGER.info("States published")

    def _listen_for_hass_started(self):
        self._hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, self._async_publish_discovery_state
        )
        async_call_later(self._hass, self._loop_time, self._async_schedule_publish)

    async def _async_schedule_publish(self, recalltime):  # pylint: disable=unused-argument
        await self._async_publish_discovery_state()
        async_call_later(self._hass, self._loop_time, self._async_schedule_publish)
