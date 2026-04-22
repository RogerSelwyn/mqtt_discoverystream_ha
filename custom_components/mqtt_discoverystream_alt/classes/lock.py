"""Lock methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components.lock import LockEntityFeature, LockState
from homeassistant.components.mqtt.const import (
    DEFAULT_PAYLOAD_LOCK,
    DEFAULT_PAYLOAD_OPEN,
    DEFAULT_PAYLOAD_UNLOCK,
)
from homeassistant.const import (
    ATTR_CODE_FORMAT,
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    SERVICE_LOCK,
    SERVICE_OPEN,
    SERVICE_UNLOCK,
    Platform,
)

from ..const import (
    COMMAND_ACTION,
    COMMAND_CODE,
    COMMAND_SET,
    CONF_CMD_T,
    CONF_CMD_TPL,
    CONF_COD_FORM,
    CONF_PL_OPEN,
    CONF_STAT_JAM,
    CONF_STAT_LOCKED,
    CONF_STAT_LOCKING,
    CONF_STAT_UNLOCKED,
    CONF_STAT_UNLOCKING,
)
from ..utils import (
    EntityInfo,
    add_config_command,
)
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Lock class."""

    PLATFORM = Platform.LOCK

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a lock."""
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)
        config[CONF_STAT_JAM] = LockState.JAMMED
        config[CONF_STAT_LOCKED] = LockState.LOCKED
        config[CONF_STAT_LOCKING] = LockState.LOCKING
        config[CONF_STAT_UNLOCKED] = LockState.UNLOCKED
        config[CONF_STAT_UNLOCKING] = LockState.UNLOCKING
        config[CONF_CMD_TPL] = (
            '{ "'
            + COMMAND_ACTION
            + '": "{{ value }}", "'
            + COMMAND_CODE
            + '":"{{ code }}" }'
        )
        if entity_info.attributes[ATTR_SUPPORTED_FEATURES] & LockEntityFeature.OPEN:
            config[CONF_PL_OPEN] = DEFAULT_PAYLOAD_OPEN
        if ATTR_CODE_FORMAT in entity_info.attributes:
            config[CONF_COD_FORM] = entity_info.attributes[ATTR_CODE_FORMAT]

    async def _async_handle_message(self, msg):
        """Handle a message for a lock."""
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
            if COMMAND_CODE in payload:
                service_payload[COMMAND_CODE] = payload[COMMAND_CODE]
            if payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_OPEN:
                await self._hass.services.async_call(
                    domain, SERVICE_OPEN, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_LOCK:
                await self._hass.services.async_call(
                    domain, SERVICE_LOCK, service_payload
                )
            elif payload[COMMAND_ACTION] == DEFAULT_PAYLOAD_UNLOCK:
                await self._hass.services.async_call(
                    domain, SERVICE_UNLOCK, service_payload
                )
            else:
                self.command_error(command, msg.payload, entity)
