"""Alarm Control Panel methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components.alarm_control_panel import (
    ATTR_CODE_ARM_REQUIRED,
    AlarmControlPanelEntityFeature,
)
from homeassistant.components.mqtt.const import (
    DEFAULT_PAYLOAD_ARM_AWAY,
    DEFAULT_PAYLOAD_ARM_CUSTOM_BYPASS,
    DEFAULT_PAYLOAD_ARM_HOME,
    DEFAULT_PAYLOAD_ARM_NIGHT,
    DEFAULT_PAYLOAD_ARM_VACATION,
    DEFAULT_PAYLOAD_DISARM,
    DEFAULT_PAYLOAD_TRIGGER,
    REMOTE_CODE,
    REMOTE_CODE_TEXT,
)
from homeassistant.const import (
    ATTR_CODE_FORMAT,
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    CONF_CODE,
    SERVICE_ALARM_ARM_AWAY,
    SERVICE_ALARM_ARM_CUSTOM_BYPASS,
    SERVICE_ALARM_ARM_HOME,
    SERVICE_ALARM_ARM_NIGHT,
    SERVICE_ALARM_ARM_VACATION,
    SERVICE_ALARM_DISARM,
    SERVICE_ALARM_TRIGGER,
    Platform,
)

from ..const import (
    ATTR_CODE_DISARM_REQUIRED,
    ATTR_CODE_TRIGGER_REQUIRED,
    COMMAND_ACTION,
    COMMAND_CODE,
    COMMAND_SET,
    CONF_CMD_T,
    CONF_CMD_TPL,
    CONF_COD_ARM_REQ,
    CONF_COD_DIS_REQ,
    CONF_COD_TRIG_REQ,
    CONF_SUP_FEAT,
)
from ..utils import (
    EntityInfo,
    add_config_command,
    simple_attribute_add,
)
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Alarm Control Panel class."""

    PLATFORM = Platform.ALARM_CONTROL_PANEL

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a alarm_control_panel."""
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)
        config[CONF_CMD_TPL] = (
            '{ "'
            + COMMAND_ACTION
            + '": "{{ action }}", "'
            + COMMAND_CODE
            + '":"{{ code }}" }'
        )
        config[CONF_SUP_FEAT] = []
        for feature in AlarmControlPanelEntityFeature:
            if entity_info.attributes[ATTR_SUPPORTED_FEATURES] & feature:
                config[CONF_SUP_FEAT].append(feature.name.lower())

        simple_attribute_add(
            config, entity_info.attributes, ATTR_CODE_ARM_REQUIRED, CONF_COD_ARM_REQ
        )
        if (
            ATTR_CODE_ARM_REQUIRED in entity_info.attributes
            and entity_info.attributes[ATTR_CODE_ARM_REQUIRED]
        ):
            if entity_info.attributes[ATTR_CODE_FORMAT] == "number":
                config[CONF_CODE] = REMOTE_CODE
            else:
                config[CONF_CODE] = REMOTE_CODE_TEXT

        simple_attribute_add(
            config, entity_info.attributes, ATTR_CODE_DISARM_REQUIRED, CONF_COD_DIS_REQ
        )
        simple_attribute_add(
            config,
            entity_info.attributes,
            ATTR_CODE_TRIGGER_REQUIRED,
            CONF_COD_TRIG_REQ,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a alarm_control_panel."""
        valid, domain, entity, command = self.validate_message(
            msg,
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        if command == COMMAND_SET:
            payload = json.loads(msg.payload)
            if COMMAND_CODE in payload and payload[COMMAND_CODE] != "None":
                service_payload[COMMAND_CODE] = payload[COMMAND_CODE]
            if payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_ARM_HOME:
                await self._hass.services.async_call(
                    domain, SERVICE_ALARM_ARM_HOME, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_ARM_AWAY:
                await self._hass.services.async_call(
                    domain, SERVICE_ALARM_ARM_AWAY, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_ARM_CUSTOM_BYPASS:
                await self._hass.services.async_call(
                    domain, SERVICE_ALARM_ARM_CUSTOM_BYPASS, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_ARM_VACATION:
                await self._hass.services.async_call(
                    domain, SERVICE_ALARM_ARM_VACATION, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_ARM_NIGHT:
                await self._hass.services.async_call(
                    domain, SERVICE_ALARM_ARM_NIGHT, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_DISARM:
                await self._hass.services.async_call(
                    domain, SERVICE_ALARM_DISARM, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_TRIGGER:
                await self._hass.services.async_call(
                    domain, SERVICE_ALARM_TRIGGER, service_payload
                )
            else:
                self.command_error(command, msg.payload, entity)
