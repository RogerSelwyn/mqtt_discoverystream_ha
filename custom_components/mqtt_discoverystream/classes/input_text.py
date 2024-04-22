"""input_text methods for MQTT Discovery Statestream."""

from homeassistant.components import mqtt
from homeassistant.components.input_text import DOMAIN as INPUT_TEXT_DOMAIN
from homeassistant.components.text import (
    ATTR_MAX,
    ATTR_MIN,
    ATTR_PATTERN,
    ATTR_VALUE,
    SERVICE_SET_VALUE,
)
from homeassistant.const import ATTR_ENTITY_ID, ATTR_STATE, STATE_UNKNOWN

from ..const import (
    ATTR_MODE,
    ATTR_SET,
    CONF_CMD_T,
    CONF_MAX,
    CONF_MIN,
    CONF_MODE,
    CONF_PATTERN,
)
from ..utils import EntityInfo, validate_message
from .entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Input_Text class."""

    PLATFORM = INPUT_TEXT_DOMAIN

    def __init__(
        self,
        hass,
        publish_retain,
        platform,
    ):
        """Initialise the input_button class."""
        super().__init__(
            hass,
            publish_retain,
            platform,
            publish_state=False,
        )

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a input_text."""
        config[CONF_CMD_T] = f"{entity_info.mycommand}{ATTR_SET}"
        config[CONF_MAX] = entity_info.attributes[ATTR_MAX]
        config[CONF_MIN] = entity_info.attributes[ATTR_MIN]
        config[CONF_MODE] = entity_info.attributes[ATTR_MODE]
        if entity_info.attributes[ATTR_PATTERN]:
            config[CONF_PATTERN] = entity_info.attributes[ATTR_PATTERN]

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a input_text."""

        if new_state.state != STATE_UNKNOWN:
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{ATTR_STATE}",
                new_state.state,
                1,
                self._publish_retain,
            )

        await super().async_publish_state(new_state, mybase)

    async def _async_handle_message(self, msg):
        """Handle a message for a input_text."""
        valid, domain, entity, command = validate_message(  # pylint: disable=unused-variable
            self._hass, msg, DiscoveryItem.PLATFORM
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_VALUE: msg.payload,
        }
        await self._hass.services.async_call(domain, SERVICE_SET_VALUE, service_payload)
