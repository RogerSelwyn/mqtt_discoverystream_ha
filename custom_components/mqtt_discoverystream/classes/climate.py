"""climate methods for MQTT Discovery Statestream."""

from homeassistant.components import mqtt
from homeassistant.components.climate import (
    ATTR_CURRENT_TEMPERATURE,
    ATTR_HVAC_ACTION,
    ATTR_HVAC_MODES,
    ATTR_MAX_TEMP,
    ATTR_MIN_TEMP,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
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
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    STATE_OFF,
    STATE_UNAVAILABLE,
    Platform,
)

from ..const import ATTR_MODE_COMMAND, ATTR_PRESET_COMMAND, ATTR_TEMP_COMMAND
from ..utils import async_publish_base_attributes


class Climate:
    """Climate class."""

    def __init__(self, hass, base_topic):
        """Initialise the climate class."""
        self._hass = hass
        self._base_topic = base_topic

    def build_config(self, config, attributes, mybase):
        """Build the config for a climate."""
        config[CONF_ACTION_TOPIC] = f"{mybase}{ATTR_HVAC_ACTION}"
        config[CONF_CURRENT_TEMP_TOPIC] = f"{mybase}{ATTR_CURRENT_TEMPERATURE}"
        config[CONF_TEMP_MAX] = attributes[ATTR_MAX_TEMP]
        config[CONF_TEMP_MIN] = attributes[ATTR_MIN_TEMP]
        config[CONF_MODE_COMMAND_TOPIC] = f"{mybase}{ATTR_MODE_COMMAND}"
        config[CONF_MODE_LIST] = attributes[ATTR_HVAC_MODES]
        config[CONF_MODE_STATE_TOPIC] = f"{mybase}{ATTR_HVAC_MODE}"
        preset_modes = attributes[ATTR_PRESET_MODES]
        if PRESET_NONE in preset_modes:
            preset_modes.remove(PRESET_NONE)
        config[CONF_PRESET_MODES_LIST] = preset_modes
        config[CONF_PRESET_MODE_COMMAND_TOPIC] = f"{mybase}{ATTR_PRESET_COMMAND}"
        config[CONF_PRESET_MODE_STATE_TOPIC] = f"{mybase}{ATTR_PRESET_MODE}"
        config[CONF_TEMP_COMMAND_TOPIC] = f"{mybase}{ATTR_TEMP_COMMAND}"
        config[CONF_TEMP_STATE_TOPIC] = f"{mybase}{ATTR_TEMPERATURE}"

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a light."""
        await self._async_publish_attribute(new_state, mybase, ATTR_HVAC_ACTION)
        await self._async_publish_attribute(new_state, mybase, ATTR_CURRENT_TEMPERATURE)
        await self._async_publish_attribute(new_state, mybase, ATTR_PRESET_MODE)
        await self._async_publish_attribute(new_state, mybase, ATTR_TEMPERATURE)

        await async_publish_base_attributes(self._hass, new_state, mybase)

        payload = new_state.state
        if payload == STATE_UNAVAILABLE:
            payload = STATE_OFF
        await mqtt.async_publish(
            self._hass, f"{mybase}{ATTR_HVAC_MODE}", payload, 1, True
        )

    async def _async_publish_attribute(self, new_state, mybase, attribute_name):
        if attribute_name in new_state.attributes:
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{attribute_name}",
                new_state.attributes[attribute_name],
                1,
                True,
            )

    async def async_subscribe(self):
        """Subscribe to messages for climate."""
        await self._hass.components.mqtt.async_subscribe(
            f"{self._base_topic}{Platform.CLIMATE}/+/{ATTR_MODE_COMMAND}",
            self._async_handle_message,
        )
        await self._hass.components.mqtt.async_subscribe(
            f"{self._base_topic}{Platform.CLIMATE}/+/{ATTR_PRESET_COMMAND}",
            self._async_handle_message,
        )
        await self._hass.components.mqtt.async_subscribe(
            f"{self._base_topic}{Platform.CLIMATE}/+/{ATTR_TEMP_COMMAND}",
            self._async_handle_message,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a switch."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]
        element = explode_topic[3]

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }

        if element == ATTR_MODE_COMMAND:
            service_payload[ATTR_HVAC_MODE] = msg.payload
            service_name = SERVICE_SET_HVAC_MODE
        elif element == ATTR_PRESET_COMMAND:
            service_payload[ATTR_PRESET_MODE] = msg.payload
            service_name = SERVICE_SET_PRESET_MODE
        elif element == ATTR_TEMP_COMMAND:
            service_payload[ATTR_TEMPERATURE] = msg.payload
            service_name = SERVICE_SET_TEMPERATURE

        await self._hass.services.async_call(domain, service_name, service_payload)
