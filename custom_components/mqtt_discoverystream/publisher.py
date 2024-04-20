"""Discovery for MQTT Discovery Stream."""

import asyncio
import logging

from homeassistant.components import mqtt
from homeassistant.components.mqtt import DOMAIN as MQTT_DOMAIN
from homeassistant.components.mqtt.const import (
    CONF_AVAILABILITY,
    CONF_TOPIC,
    DEFAULT_PAYLOAD_AVAILABLE,
    DEFAULT_PAYLOAD_NOT_AVAILABLE,
)
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STARTED,
    EVENT_HOMEASSISTANT_STOP,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.helpers import entity_registry
from homeassistant.helpers.entityfilter import convert_include_exclude_filter
from homeassistant.helpers.event import async_call_later
from homeassistant.setup import async_when_setup

from .const import (
    CONF_BASE_TOPIC,
    CONF_ONLINE_STATUS,
    CONF_PUBLISHED,
    CONF_REMOTE_STATUS,
    CONF_REPUBLISH_TIME,
    DEFAULT_STATE_SLEEP,
    DOMAIN,
)
from .discovery import Discovery

_LOGGER = logging.getLogger(__name__)


class Publisher:
    """Manage publication for MQTT Discovery Statestream."""

    def __init__(self, hass, conf, base_topic, publish_retain):
        """Initiate publishing."""
        self._hass = hass
        self._base_topic = base_topic
        self._publish_retain = publish_retain
        self._conf = conf
        self._remote_status, self._remote_status_topic = self._set_remote_status()
        self._hass.data[DOMAIN] = {CONF_PUBLISHED: []}
        self.discovery = Discovery(self._hass, self._conf)
        self._entity_states = {}
        if self._remote_status:
            async_when_setup(hass, MQTT_DOMAIN, self._async_birth_subscribe)
        self._register_services()
        self._listen_for_hass_events()
        self._subscribed = []

    async def async_state_publish(self, entity_id, new_state, mybase):
        """Publish state for MQTT Discovery Statestream."""
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if entity_id not in self._hass.data[DOMAIN][CONF_PUBLISHED]:
            await self.discovery.async_discovery_publish(
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

        entityclass = self.discovery.discovery_classes[ent_domain]
        await entityclass.async_publish_state(new_state, mybase)

        await mqtt.async_publish(
            self._hass,
            f"{mybase}{CONF_AVAILABILITY}",
            DEFAULT_PAYLOAD_AVAILABLE,
            1,
            self._publish_retain,
        )

    async def _async_birth_subscribe(self, hass, component):  # pylint: disable=unused-argument
        """Subscribe birth messages."""
        await mqtt.async_subscribe(
            self._hass,
            f"{self._remote_status_topic}",
            self._async_handle_birth_message,
        )

    async def _async_handle_birth_message(self, msg):
        if msg.payload == self._remote_status.get(CONF_ONLINE_STATUS):
            await self._async_publish_discovery_state()

    def _register_services(self):
        self._hass.services.async_register(
            DOMAIN, "publish_discovery_state", self._async_publish_discovery_state
        )

    def _listen_for_hass_events(self):
        self._hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, self._async_publish_discovery_state
        )
        self._hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, self._async_mark_unavailable
        )

        async_call_later(
            self._hass,
            self._conf.get(CONF_REPUBLISH_TIME),
            self._async_schedule_publish,
        )

    async def _async_publish_discovery_state(self, call=None):  # pylint: disable=unused-argument
        ent_reg = entity_registry.async_get(self._hass)
        self._entity_states = {}
        publish_filter = convert_include_exclude_filter(self._conf)
        for entity_id in list(ent_reg.entities):
            if publish_filter(entity_id):
                if current_state := self._hass.states.get(entity_id):
                    mybase = f"{self._base_topic}{entity_id.replace('.', '/')}/"
                    await self.discovery.async_discovery_publish(
                        entity_id, current_state.attributes, mybase
                    )
                    self._entity_states[entity_id] = current_state

        _LOGGER.debug("Discovery published")
        await asyncio.sleep(DEFAULT_STATE_SLEEP)
        for entity_id, current_state in self._entity_states.items():
            mybase = f"{self._base_topic}{entity_id.replace('.', '/')}/"
            await self.async_state_publish(entity_id, current_state, mybase)
        _LOGGER.debug("States published")

    async def _async_mark_unavailable(self, call):  # pylint: disable=unused-argument
        _LOGGER.info("Shutdown - marking entities unavailable")
        for entity_id in self._entity_states:
            mybase = f"{self._base_topic}{entity_id.replace('.', '/')}/"
            _LOGGER.info(entity_id)
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{CONF_AVAILABILITY}",
                DEFAULT_PAYLOAD_NOT_AVAILABLE,
                0,
                self._publish_retain,
            )

    async def _async_schedule_publish(self, recalltime):  # pylint: disable=unused-argument
        await self._async_publish_discovery_state()
        async_call_later(
            self._hass,
            self._conf.get(CONF_REPUBLISH_TIME),
            self._async_schedule_publish,
        )

    def _set_remote_status(self):
        remote_status = self._conf.get(CONF_REMOTE_STATUS)
        remote_status_topic = None
        if remote_status:
            remote_status_topic = remote_status.get(CONF_TOPIC) or self._conf.get(
                CONF_BASE_TOPIC
            )
            if not remote_status_topic.endswith("/status"):
                remote_status_topic = f"{remote_status_topic}/status"
        return remote_status, remote_status_topic
