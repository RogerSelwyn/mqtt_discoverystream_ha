"""Discovery for MQTT Discovery Stream."""
import json
import logging
from datetime import timedelta

from homeassistant.components import mqtt
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_INCLUDE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
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
from .const import CONF_BASE_TOPIC, CONF_DISCOVERY_TOPIC, CONF_JSON_ATTRS_TOPIC, DOMAIN
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
        self._hass.data[DOMAIN][self._discovery_topic]["conf_published"] = []
        self._binary_sensor = BinarySensor()
        self._climate = Climate(hass)
        self._light = Light(hass)
        self._switch = Switch()
        self._publish_filter = convert_include_exclude_filter(conf)
        hass.async_create_task(self._async_subscribe(None))

    async def async_state_publish(self, entity_id, new_state, mybase):
        """Publish state for MQTT Duscovery Statestream."""
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if (
            entity_id
            not in self._hass.data[DOMAIN][self._discovery_topic]["conf_published"]
        ):
            await self._async_discovery_publish(entity_id, new_state.attributes, mybase)

        if ent_domain == "light":
            await self._light.async_publish_state(new_state, mybase)
        elif ent_domain == "climate":
            await self._climate.async_publish_state(new_state, mybase)
        else:
            await async_publish_base_attributes(self._hass, new_state, mybase)

        payload = (
            "offline"
            if new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, None)
            else "online"
        )
        await mqtt.async_publish(self._hass, f"{mybase}availability", payload, 1, True)

    async def _async_discovery_publish(self, entity_id, attributes, mybase):
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        config = self._build_base(entity_id, attributes, mybase)

        publish_config = False
        if ent_domain == "sensor" and (
            self._has_includes or "device_class" in attributes
        ):
            publish_config = True

        elif ent_domain == "binary_sensor" and (
            self._has_includes or "device_class" in attributes
        ):
            self._binary_sensor.build_config(config)
            publish_config = True

        elif ent_domain == "switch":
            self._switch.build_config(config, mybase)
            publish_config = True

        elif ent_domain == "device_tracker":
            publish_config = True

        elif ent_domain == "climate":
            self._climate.build_config(config, attributes, mybase)
            publish_config = True

        elif ent_domain == "light":
            self._light.build_config(config, entity_id, attributes, mybase)
            publish_config = True

        if publish_config:
            if device := self._build_device(entity_id):
                config["dev"] = device

            encoded = json.dumps(config, cls=JSONEncoder)
            entity_disc_topic = (
                f"{self._discovery_topic}{entity_id.replace('.', '/')}/config"
            )
            await mqtt.async_publish(self._hass, entity_disc_topic, encoded, 1, True)
            self._hass.data[DOMAIN][self._discovery_topic]["conf_published"].append(
                entity_id
            )

    def _build_base(self, entity_id, attributes, mybase):
        ent_parts = entity_id.split(".")
        ent_id = ent_parts[1]

        config = {
            "uniq_id": f"mqtt_{entity_id}",
            "name": ent_id.replace("_", " ").title(),
            "stat_t": f"{mybase}state",
            CONF_JSON_ATTRS_TOPIC: f"{mybase}attributes",
            "avty_t": f"{mybase}availability",
        }
        if "device_class" in attributes:
            config["dev_cla"] = attributes["device_class"]
        if "unit_of_measurement" in attributes:
            config["unit_of_meas"] = attributes["unit_of_measurement"]
        if "state_class" in attributes:
            config["stat_cla"] = attributes["state_class"]
        if "icon" in attributes:
            config["icon"] = attributes["icon"]

        return config

    def _build_device(self, entity_id):  # sourcery skip: extract-method
        config_device = {}
        entry = self._ent_reg.async_get(entity_id)
        if entry and entry.device_id:
            if device := self._dev_reg.async_get(entry.device_id):
                if device.manufacturer:
                    config_device["mf"] = device.manufacturer
                if device.model:
                    config_device["mdl"] = device.model
                if device.name:
                    config_device["name"] = device.name
                if device.sw_version:
                    config_device["sw"] = device.sw_version
                if device.identifiers:
                    config_device["ids"] = [id[1] for id in device.identifiers]
                if device.connections:
                    config_device["cns"] = device.connections

        return config_device

    async def _async_subscribe(self, recalltime):  # pylint: disable=unused-argument
        """Subscribe to neccesary topics as part MQTT Discovery Statestream."""
        try:
            await self._hass.components.mqtt.async_subscribe(
                f"{self._base_topic}switch/+/set", self._async_message_received
            )
            await self._hass.components.mqtt.async_subscribe(
                f"{self._base_topic}light/+/set_light", self._async_message_received
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
        if element == "set":
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
                    'Invalid service for "set" - payload: %s for %s',
                    {msg.payload},
                    {entity},
                )
        elif element == "set_light":
            await self._light.async_handle_message(domain, entity, msg)
