"""climate methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components import mqtt
from homeassistant.components.climate import (
    ATTR_CURRENT_TEMPERATURE,
    ATTR_HVAC_ACTION,
    ATTR_HVAC_MODES,
    ATTR_MAX_TEMP,
    ATTR_MIN_TEMP,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    ATTR_TARGET_TEMP_STEP,
    PRESET_NONE,
    SERVICE_SET_HVAC_MODE,
    SERVICE_SET_PRESET_MODE,
    SERVICE_SET_TEMPERATURE,
)
from homeassistant.components.mqtt.climate import (
    ATTR_HVAC_MODE,
    CONF_ACTION_TOPIC,
    CONF_CURRENT_TEMP_TOPIC,
    CONF_MODE_COMMAND_TOPIC,
    CONF_MODE_LIST,
    CONF_MODE_STATE_TOPIC,
    CONF_PRESET_MODE_COMMAND_TOPIC,
    CONF_PRESET_MODE_STATE_TOPIC,
    CONF_PRESET_MODES_LIST,
    CONF_TEMP_COMMAND_TOPIC,
    CONF_TEMP_MAX,
    CONF_TEMP_MIN,
    CONF_TEMP_STATE_TOPIC,
    CONF_TEMP_STEP,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    STATE_OFF,
    STATE_UNAVAILABLE,
    Platform,
)

from ..const import (
    ATTR_MODE_COMMAND,
    ATTR_PRESET_COMMAND,
    ATTR_TEMP_COMMAND,
    CONF_STAT_T,
)
from ..utils import EntityInfo, async_publish_attribute, validate_message
from .entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Climate class."""

    PLATFORM = Platform.CLIMATE

    def __init__(
        self,
        hass,
        publish_retain,
        platform,
    ):
        """Initialise the climate class."""
        super().__init__(
            hass,
            publish_retain,
            platform,
            publish_state=False,
        )

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a climate."""
        del config[CONF_STAT_T]
        config[CONF_ACTION_TOPIC] = f"{entity_info.mybase}{ATTR_HVAC_ACTION}"
        config[CONF_CURRENT_TEMP_TOPIC] = (
            f"{entity_info.mybase}{ATTR_CURRENT_TEMPERATURE}"
        )
        config[CONF_TEMP_MAX] = entity_info.attributes[ATTR_MAX_TEMP]
        config[CONF_TEMP_MIN] = entity_info.attributes[ATTR_MIN_TEMP]
        config[CONF_MODE_COMMAND_TOPIC] = f"{entity_info.mycommand}{ATTR_MODE_COMMAND}"
        config[CONF_MODE_LIST] = entity_info.attributes[ATTR_HVAC_MODES]
        config[CONF_MODE_STATE_TOPIC] = f"{entity_info.mybase}{ATTR_HVAC_MODE}"
        preset_modes = entity_info.attributes[ATTR_PRESET_MODES]
        if PRESET_NONE in preset_modes:
            preset_modes.remove(PRESET_NONE)
        config[CONF_PRESET_MODES_LIST] = preset_modes
        config[CONF_PRESET_MODE_COMMAND_TOPIC] = (
            f"{entity_info.mycommand}{ATTR_PRESET_COMMAND}"
        )
        config[CONF_PRESET_MODE_STATE_TOPIC] = f"{entity_info.mybase}{ATTR_PRESET_MODE}"
        config[CONF_TEMP_COMMAND_TOPIC] = f"{entity_info.mycommand}{ATTR_TEMP_COMMAND}"
        config[CONF_TEMP_STATE_TOPIC] = f"{entity_info.mybase}{ATTR_TEMPERATURE}"
        config[CONF_TEMP_STEP] = (
            entity_info.attributes[ATTR_TARGET_TEMP_STEP]
            if ATTR_TARGET_TEMP_STEP in entity_info.attributes
            else 0.5
        )

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a climate."""
        _LOGGER.debug("New State %s;", new_state)
        await async_publish_attribute(
            self._hass, new_state, mybase, ATTR_HVAC_ACTION, self._publish_retain
        )
        await async_publish_attribute(
            self._hass,
            new_state,
            mybase,
            ATTR_CURRENT_TEMPERATURE,
            self._publish_retain,
        )
        await async_publish_attribute(
            self._hass, new_state, mybase, ATTR_PRESET_MODE, self._publish_retain
        )
        await async_publish_attribute(
            self._hass, new_state, mybase, ATTR_TEMPERATURE, self._publish_retain
        )

        await super().async_publish_state(new_state, mybase)

        payload = new_state.state
        if payload == STATE_UNAVAILABLE:
            payload = STATE_OFF
        await mqtt.async_publish(
            self._hass, f"{mybase}{ATTR_HVAC_MODE}", payload, 1, self._publish_retain
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a switch."""
        valid, domain, entity, command = validate_message(
            self._hass, msg, DiscoveryItem.PLATFORM
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }

        if command == ATTR_MODE_COMMAND:
            service_payload[ATTR_HVAC_MODE] = msg.payload
            service_name = SERVICE_SET_HVAC_MODE
        elif command == ATTR_PRESET_COMMAND:
            service_payload[ATTR_PRESET_MODE] = msg.payload
            service_name = SERVICE_SET_PRESET_MODE
        elif command == ATTR_TEMP_COMMAND:
            service_payload[ATTR_TEMPERATURE] = msg.payload
            service_name = SERVICE_SET_TEMPERATURE

        await self._hass.services.async_call(domain, service_name, service_payload)
