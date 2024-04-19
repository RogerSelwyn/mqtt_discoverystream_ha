"""Publishing for MQTT Discovery Stream."""

import json

from homeassistant.components import mqtt
from homeassistant.components.mqtt.const import (
    CONF_AVAILABILITY,
    CONF_TOPIC,
    DATA_MQTT,
)
from homeassistant.components.mqtt.mixins import (
    AVAILABILITY_LATEST,
    CONF_PAYLOAD_AVAILABLE,
    CONF_PAYLOAD_NOT_AVAILABLE,
)
from homeassistant.components.sensor import ATTR_STATE_CLASS
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_FRIENDLY_NAME,
    ATTR_ICON,
    ATTR_STATE,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_INCLUDE,
    CONF_NAME,
    Platform,
)
from homeassistant.helpers import device_registry, entity_registry
from homeassistant.helpers.json import JSONEncoder

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_CONFIG,
    CONF_AVTY,
    CONF_AVTY_MODE,
    CONF_BASE_TOPIC,
    CONF_CNS,
    CONF_COMMAND_TOPIC,
    CONF_DEV,
    CONF_DEV_CLA,
    CONF_DISCOVERY_TOPIC,
    CONF_ENT_CAT,
    CONF_IDS,
    CONF_JSON_ATTR_T,
    CONF_LOCAL_STATUS,
    CONF_MDL,
    CONF_MF,
    CONF_OBJ_ID,
    CONF_OFFLINE_STATUS,
    CONF_ONLINE_STATUS,
    CONF_PUBLISH_RETAIN,
    CONF_PUBLISHED,
    CONF_STAT_CLA,
    CONF_STAT_T,
    CONF_SW,
    CONF_UNIQ_ID,
    CONF_UNIT_OF_MEAS,
    DOMAIN,
    SUPPORTED_ENTITIES,
)
from .utils import EntityInfo, set_topic, translate_entity_type


class Discovery:
    """Manage discovery publication for MQTT Discovery Statestream."""

    def __init__(self, hass, conf, discovery_classes):
        """Initiate discovery."""
        self._hass = hass
        self._conf = conf
        self._discovery_classes = discovery_classes
        self._publish_retain: bool = conf.get(CONF_PUBLISH_RETAIN)
        self._command_topic = set_topic(conf, CONF_COMMAND_TOPIC)
        (
            self._local_status,
            self._local_status_topic,
            self._local_online_status,
            self._local_offline_status,
        ) = self._set_local_status()

        self._has_includes = bool(conf.get(CONF_INCLUDE))
        self._dev_reg = device_registry.async_get(hass)
        self._ent_reg = entity_registry.async_get(hass)
        self._discovery_topic = set_topic(conf, CONF_DISCOVERY_TOPIC)

    async def async_discovery_publish(self, entity_id, attributes, mybase):
        """Publish Discovery information for entitiy."""
        mycommand = f"{self._command_topic}{entity_id.replace('.', '/')}/"
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if ent_domain not in SUPPORTED_ENTITIES:
            return

        if (
            ent_domain in [Platform.BINARY_SENSOR, Platform.SENSOR]
            and not self._has_includes
            and ATTR_DEVICE_CLASS not in attributes
        ):
            return

        entity_info = EntityInfo(mycommand, attributes, mybase, entity_id)
        config = self._build_base(entity_info)

        entityclass = getattr(self._discovery_classes, ent_domain)
        entityclass.build_config(config, entity_info)

        if device := self._build_device(entity_id):
            config[CONF_DEV] = device

        self._hass.data[DOMAIN][CONF_PUBLISHED].append(entity_id)

        entity_id = translate_entity_type(entity_id)

        encoded = json.dumps(config, cls=JSONEncoder)
        entity_disc_topic = (
            f"{self._discovery_topic}{entity_id.replace('.', '/')}/{ATTR_CONFIG}"
        )
        await mqtt.async_publish(
            self._hass, entity_disc_topic, encoded, 1, self._publish_retain
        )

    def _build_base(self, entity_info: EntityInfo):
        # sourcery skip: assign-if-exp, merge-dict-assign
        ent_parts = entity_info.entity_id.split(".")
        ent_id = ent_parts[1]
        availability = [{CONF_TOPIC: f"{entity_info.mybase}{CONF_AVAILABILITY}"}]
        if self._local_status:
            availability.append(
                {
                    CONF_TOPIC: self._local_status_topic,
                    CONF_PAYLOAD_AVAILABLE: self._local_online_status,
                    CONF_PAYLOAD_NOT_AVAILABLE: self._local_offline_status,
                }
            )

        config = {
            CONF_UNIQ_ID: f"{DATA_MQTT}_{translate_entity_type(entity_info.entity_id)}",
            CONF_OBJ_ID: ent_id,
            CONF_STAT_T: f"{entity_info.mybase}{ATTR_STATE}",
            CONF_JSON_ATTR_T: f"{entity_info.mybase}{ATTR_ATTRIBUTES}",
            CONF_AVTY: availability,
            CONF_AVTY_MODE: AVAILABILITY_LATEST,
        }
        name = None
        if ATTR_FRIENDLY_NAME in entity_info.attributes:
            name = entity_info.attributes[ATTR_FRIENDLY_NAME]
        else:
            name = ent_id.replace("_", " ").title()
        if entry := self._ent_reg.async_get(entity_info.entity_id):
            if entry.device_id and name:
                device = self._dev_reg.async_get(entry.device_id)
                if device and name.startswith(device.name):
                    name = name[len(device.name) + 1 :].strip()
                    if name == "":
                        name = None
            if entry.entity_category:
                config[CONF_ENT_CAT] = entry.entity_category
            if entry.original_device_class:
                config[CONF_DEV_CLA] = entry.original_device_class
            elif entry.device_class:
                config[CONF_DEV_CLA] = entry.device_class
        config[CONF_NAME] = name

        if ATTR_UNIT_OF_MEASUREMENT in entity_info.attributes:
            config[CONF_UNIT_OF_MEAS] = entity_info.attributes[ATTR_UNIT_OF_MEASUREMENT]
        if ATTR_STATE_CLASS in entity_info.attributes:
            config[CONF_STAT_CLA] = entity_info.attributes[ATTR_STATE_CLASS]
        if ATTR_ICON in entity_info.attributes:
            config[ATTR_ICON] = entity_info.attributes[ATTR_ICON]

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

    def _set_local_status(self):
        local_status = self._conf.get(CONF_LOCAL_STATUS)
        local_status_topic = None
        local_online_status = None
        local_offline_status = None
        if local_status:
            local_status_topic = local_status.get(CONF_TOPIC) or self._conf.get(
                CONF_BASE_TOPIC
            )
            local_online_status = local_status.get(CONF_ONLINE_STATUS)
            local_offline_status = local_status.get(CONF_OFFLINE_STATUS)
            if not local_status_topic.endswith("/status"):
                local_status_topic = f"{local_status_topic}/status"

        return (
            local_status,
            local_status_topic,
            local_online_status,
            local_offline_status,
        )
