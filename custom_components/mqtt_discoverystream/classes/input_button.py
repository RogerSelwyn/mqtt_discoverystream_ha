"""input_button methods for MQTT Discovery Statestream."""

from homeassistant.components.button.const import SERVICE_PRESS
from homeassistant.components.input_button import DOMAIN as INPUT_BUTTON_DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
)

from ..const import (
    ATTR_PRESS,
    CONF_CMD_T,
    CONF_STAT_T,
)
from ..utils import EntityInfo, validate_message
from .base_entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Input_Button class."""

    PLATFORM = INPUT_BUTTON_DOMAIN

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
        """Build the config for a input_button."""
        del config[CONF_STAT_T]
        config[CONF_CMD_T] = f"{entity_info.mycommand}{ATTR_PRESS}"

    async def _async_handle_message(self, msg):
        """Handle a message for a input_button."""
        valid, domain, entity, command = validate_message(  # pylint: disable=unused-variable
            self._hass, msg, DiscoveryItem.PLATFORM
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        await self._hass.services.async_call(domain, SERVICE_PRESS, service_payload)
