"""Discovery for MQTT Discovery Stream."""
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
    DOMAIN,
)
from .discovery import Discovery
from .utils import async_publish_base_attributes

_LOGGER = logging.getLogger(__name__)


class Publisher:
    """Manage publication for MQTT Discovery Statestream."""

    def __init__(self, hass, conf, base_topic):
        """Initiate publishing."""
        self._hass = hass
        self._base_topic = base_topic
        self._has_includes = bool(conf.get(CONF_INCLUDE))
        self._discovery_topic = conf.get(CONF_DISCOVERY_TOPIC) or conf.get(
            CONF_BASE_TOPIC
        )
        self._command_topic = conf.get(CONF_COMMAND_TOPIC) or conf.get(CONF_BASE_TOPIC)
        if not self._command_topic.endswith("/"):
            self._command_topic = f"{self._command_topic}/"
        self._lwt_topic = conf.get(CONF_BIRTH_TOPIC) or conf.get(CONF_BASE_TOPIC)
        if not self._lwt_topic.endswith("/status"):
            self._lwt_topic = f"{self._lwt_topic}/status"
        self._hass.data[DOMAIN] = {CONF_PUBLISHED: []}
        self._climate = Climate(hass)
        self._light = Light(hass)
        self._switch = Switch(hass)
        self._cover = Cover(hass)
        self._discovery = Discovery(hass, conf)
        self._publish_filter = convert_include_exclude_filter(conf)
        async_when_setup(hass, MQTT_DOMAIN, self._async_subscribe)
        self._register_services()
        self._listen_for_hass_started()

    async def async_state_publish(self, entity_id, new_state, force_discovery=False):
        """Publish state for MQTT Discovery Statestream."""
        mybase = f"{self._base_topic}{entity_id.replace('.', '/')}/"
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if entity_id not in self._hass.data[DOMAIN][CONF_PUBLISHED] or force_discovery:
            await self._discovery.async_discovery_publish(
                entity_id, new_state.attributes, mybase
            )

        if new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, None):
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{CONF_AVAILABILITY}",
                DEFAULT_PAYLOAD_NOT_AVAILABLE,
                1,
                True,
            )
            return

        if ent_domain == Platform.LIGHT:
            await self._light.async_publish_state(new_state, mybase)
        elif ent_domain == Platform.CLIMATE:
            await self._climate.async_publish_state(new_state, mybase)
        elif ent_domain == Platform.COVER:
            await self._cover.async_publish_state(new_state, mybase)
        else:
            await async_publish_base_attributes(self._hass, new_state, mybase)

        await mqtt.async_publish(
            self._hass,
            f"{mybase}{CONF_AVAILABILITY}",
            DEFAULT_PAYLOAD_AVAILABLE,
            1,
            True,
        )

    async def _async_subscribe(self, hass, component):  # pylint: disable=unused-argument
        """Subscribe to neccesary topics as part MQTT Discovery Statestream."""
        await self._climate.async_subscribe(self._command_topic)
        await self._light.async_subscribe(self._command_topic)
        await self._switch.async_subscribe(self._command_topic)
        await self._cover.async_subscribe(self._command_topic)
        await self._async_lwt_subscribe()
        _LOGGER.info("MQTT subscribe successful")

    async def _async_lwt_subscribe(self):
        """Subscribe to lwt messages."""
        await mqtt.async_subscribe(
            self._hass,
            f"{self._lwt_topic}",
            self._async_handle_lwt_message,
        )

    async def _async_handle_lwt_message(self, msg):
        if msg.payload == "online":
            await self._async_run_discovery()

    def _register_services(self):
        self._hass.services.async_register(
            DOMAIN, "publish_discovery_state", self._async_publish_discovery_state
        )

    async def _async_publish_discovery_state(self, call=None):  # pylint: disable=unused-argument
        ent_reg = entity_registry.async_get(self._hass)
        for entity_id in ent_reg.entities:
            if self._publish_filter(entity_id):
                if current_state := self._hass.states.get(entity_id):
                    await self.async_state_publish(
                        entity_id, current_state, force_discovery=True
                    )
        _LOGGER.info("Discovery and states published")

    def _listen_for_hass_started(self):
        self._hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, self._async_run_discovery
        )

    async def _async_run_discovery(self, call=None):  # pylint: disable=unused-argument
        await self._async_publish_discovery_state()
