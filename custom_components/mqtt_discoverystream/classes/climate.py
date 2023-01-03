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
)
from homeassistant.components.mqtt.climate import (
    ATTR_HVAC_MODE,
    CONF_ACTION_TOPIC,
    CONF_CURRENT_TEMP_TOPIC,
    CONF_MODE_LIST,
    CONF_MODE_STATE_TOPIC,
    CONF_PRESET_MODE_COMMAND_TOPIC,
    CONF_PRESET_MODE_STATE_TOPIC,
    CONF_PRESET_MODES_LIST,
    CONF_TEMP_MAX,
    CONF_TEMP_MIN,
    CONF_TEMP_STATE_TOPIC,
)
from homeassistant.const import ATTR_TEMPERATURE, STATE_OFF, STATE_UNAVAILABLE

from ..const import ATTR_PRESET_COMMAND
from ..utils import async_publish_base_attributes


class Climate:
    """Climate class."""

    def __init__(self, hass):
        """Initialise the climate class."""
        self._hass = hass

    def build_config(self, config, attributes, mybase):
        """Build the config for a climate."""
        config[CONF_ACTION_TOPIC] = f"{mybase}{ATTR_HVAC_ACTION}"
        config[CONF_CURRENT_TEMP_TOPIC] = f"{mybase}{ATTR_CURRENT_TEMPERATURE}"
        config[CONF_TEMP_MAX] = attributes[ATTR_MAX_TEMP]
        config[CONF_TEMP_MIN] = attributes[ATTR_MIN_TEMP]
        config[CONF_MODE_LIST] = attributes[ATTR_HVAC_MODES]
        config[CONF_MODE_STATE_TOPIC] = f"{mybase}{ATTR_HVAC_MODE}"
        preset_modes = attributes[ATTR_PRESET_MODES]
        if PRESET_NONE in preset_modes:
            preset_modes.remove(PRESET_NONE)
        config[CONF_PRESET_MODES_LIST] = preset_modes
        config[CONF_PRESET_MODE_COMMAND_TOPIC] = f"{mybase}{ATTR_PRESET_COMMAND}"
        config[CONF_PRESET_MODE_STATE_TOPIC] = f"{mybase}{ATTR_PRESET_MODE}"
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
