"""Discovery for MQTT Discovery Stream."""
import json
import logging
from datetime import timedelta

from homeassistant.components import mqtt
from homeassistant.components.mqtt.const import (
    CONF_AVAILABILITY,
    DATA_MQTT,
    DEFAULT_PAYLOAD_AVAILABLE,
    DEFAULT_PAYLOAD_NOT_AVAILABLE,
)
from homeassistant.components.sensor import ATTR_STATE_CLASS
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ENTITY_ID,
    ATTR_FRIENDLY_NAME,
    ATTR_ICON,
    ATTR_STATE,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_INCLUDE,
    CONF_NAME,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    Platform,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry, entity_registry
from homeassistant.helpers.entityfilter import convert_include_exclude_filter
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.json import JSONEncoder

from .classes.binary_sensor import BinarySensor
from .classes.climate import Climate
from .classes.light import Light
from .classes.switch import Switch
from .const import (
    ATTR_ATTRIBUTES,
    ATTR_CONFIG,
    ATTR_SET,
    ATTR_SET_LIGHT,
    CONF_AVTY_T,
    CONF_BASE_TOPIC,
    CONF_CNS,
    CONF_DEV,
    CONF_DEV_CLA,
    CONF_DISCOVERY_TOPIC,
    CONF_IDS,
    CONF_JSON_ATTR_T,
    CONF_MDL,
    CONF_MF,
    CONF_OBJ_ID,
    CONF_PUBLISHED,
    CONF_STAT_CLA,
    CONF_STAT_T,
    CONF_SW,
    CONF_UNIQ_ID,
    CONF_UNIT_OF_MEAS,
    DOMAIN,
)
from .utils import async_publish_base_attributes

_LOGGER = logging.getLogger(__name__)


class Discovery:
    """Manage discovery publication for MQTT Discovery Statestream."""

    def __init__(self, hass, base_topic, conf):
        """Initiate discovery."""
        self._hass = hass
        self._base_topic = base_topic
        self._has_includes = bool(conf.get(CONF_INCLUDE))
        self._discovery_topic = conf.get(CONF_DISCOVERY_TOPIC) or conf.get(
            CONF_BASE_TOPIC
        )
        self._dev_reg = device_registry.async_get(hass)
        self._ent_reg = entity_registry.async_get(hass)
        if not self._discovery_topic.endswith("/"):
            self._discovery_topic = f"{self._discovery_topic}/"
        self._hass.data[DOMAIN] = {self._discovery_topic: {}}
        self._hass.data[DOMAIN][self._discovery_topic][CONF_PUBLISHED] = []
        self._binary_sensor = BinarySensor()
        self._climate = Climate(hass)
        self._light = Light(hass)
        self._switch = Switch()
        self._publish_filter = convert_include_exclude_filter(conf)
        hass.async_create_task(self._async_subscribe(None))

    async def async_state_publish(self, entity_id, new_state, mybase):
        """Publish state for MQTT Discovery Statestream."""
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if (
            entity_id
            not in self._hass.data[DOMAIN][self._discovery_topic][CONF_PUBLISHED]
        ):
            await self._async_discovery_publish(entity_id, new_state.attributes, mybase)

        if ent_domain == Platform.LIGHT:
            await self._light.async_publish_state(new_state, mybase)
        elif ent_domain == Platform.CLIMATE:
            await self._climate.async_publish_state(new_state, mybase)
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

    async def _async_discovery_publish(self, entity_id, attributes, mybase):
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        config = self._build_base(entity_id, attributes, mybase)

        publish_config = False
        if ent_domain == Platform.SENSOR and (
            self._has_includes or ATTR_DEVICE_CLASS in attributes
        ):
            publish_config = True

        elif ent_domain == Platform.BINARY_SENSOR and (
            self._has_includes or ATTR_DEVICE_CLASS in attributes
        ):
            self._binary_sensor.build_config(config)
            publish_config = True

        elif ent_domain == Platform.SWITCH:
            self._switch.build_config(config, mybase)
            publish_config = True

        elif ent_domain == Platform.DEVICE_TRACKER:
            publish_config = True

        elif ent_domain == Platform.CLIMATE:
            self._climate.build_config(config, attributes, mybase)
            publish_config = True

        elif ent_domain == Platform.LIGHT:
            self._light.build_config(config, entity_id, attributes, mybase)
            publish_config = True

        if publish_config:
            if device := self._build_device(entity_id):
                config[CONF_DEV] = device

            encoded = json.dumps(config, cls=JSONEncoder)
            entity_disc_topic = (
                f"{self._discovery_topic}{entity_id.replace('.', '/')}/{ATTR_CONFIG}"
            )
            await mqtt.async_publish(self._hass, entity_disc_topic, encoded, 1, True)
            self._hass.data[DOMAIN][self._discovery_topic][CONF_PUBLISHED].append(
                entity_id
            )

    def _build_base(self, entity_id, attributes, mybase):
        ent_parts = entity_id.split(".")
        ent_id = ent_parts[1]

        config = {
            CONF_UNIQ_ID: f"{DATA_MQTT}_{entity_id}",
            CONF_OBJ_ID: ent_id,
            CONF_STAT_T: f"{mybase}{ATTR_STATE}",
            CONF_JSON_ATTR_T: f"{mybase}{ATTR_ATTRIBUTES}",
            CONF_AVTY_T: f"{mybase}{CONF_AVAILABILITY}",
        }

        if ATTR_FRIENDLY_NAME in attributes:
            config[CONF_NAME] = attributes[ATTR_FRIENDLY_NAME]
        else:
            config[CONF_NAME] = ent_id.replace("_", " ").title()
        if ATTR_DEVICE_CLASS in attributes:
            config[CONF_DEV_CLA] = attributes[ATTR_DEVICE_CLASS]
        if ATTR_UNIT_OF_MEASUREMENT in attributes:
            config[CONF_UNIT_OF_MEAS] = attributes[ATTR_UNIT_OF_MEASUREMENT]
        if ATTR_STATE_CLASS in attributes:
            config[CONF_STAT_CLA] = attributes[ATTR_STATE_CLASS]
        if ATTR_ICON in attributes:
            config[ATTR_ICON] = attributes[ATTR_ICON]

        return config

    def _build_device(self, entity_id):  # sourcery skip: extract-method
        config_device = {}
        entry = self._ent_reg.async_get(entity_id)
        if entry and entry.device_id:
            if device := self._dev_reg.async_get(entry.device_id):
                if device.manufacturer:
                    config_device[CONF_MF] = device.manufacturer
                if device.model:
                    config_device[CONF_MDL] = device.model
                if device.name:
                    config_device[CONF_NAME] = device.name
                if device.sw_version:
                    config_device[CONF_SW] = device.sw_version
                if device.identifiers:
                    config_device[CONF_IDS] = [id[1] for id in device.identifiers]
                if device.connections:
                    config_device[CONF_CNS] = device.connections

        return config_device

    async def _async_subscribe(self, recalltime):  # pylint: disable=unused-argument
        """Subscribe to neccesary topics as part MQTT Discovery Statestream."""
        try:
            await self._hass.components.mqtt.async_subscribe(
                f"{self._base_topic}{Platform.SWITCH}/+/{ATTR_SET}",
                self._async_message_received,
            )
            await self._hass.components.mqtt.async_subscribe(
                f"{self._base_topic}{Platform.LIGHT}/+/{ATTR_SET_LIGHT}",
                self._async_message_received,
            )
            _LOGGER.info("MQTT subscribe successful")
        except HomeAssistantError:
            seconds = 10
            retrytime = timedelta(seconds=seconds)
            _LOGGER.warning(
                "MQTT subscribe unsuccessful - retrying in %s seconds", seconds
            )
            async_call_later(self._hass, retrytime, self._async_subscribe)

    async def _async_message_received(self, msg):
        """Handle new messages on MQTT."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]
        element = explode_topic[3]

        _LOGGER.debug(
            "Message received: topic %s; payload: %s", {msg.topic}, {msg.payload}
        )
        if element == ATTR_SET:
            if msg.payload == STATE_ON:
                await self._hass.services.async_call(
                    domain, SERVICE_TURN_ON, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
                )
            elif msg.payload == STATE_OFF:
                await self._hass.services.async_call(
                    domain, SERVICE_TURN_OFF, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
                )
            else:
                _LOGGER.error(
                    'Invalid service for "%s" - payload: %s for %s',
                    ATTR_SET,
                    {msg.payload},
                    {entity},
                )
        elif element == ATTR_SET_LIGHT:
            await self._light.async_handle_message(domain, entity, msg)
