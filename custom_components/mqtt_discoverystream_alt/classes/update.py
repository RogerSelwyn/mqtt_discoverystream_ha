"""Update methods for MQTT Discovery Statestream."""

from homeassistant.components import mqtt
from homeassistant.components.mqtt.update import (
    CONF_DISPLAY_PRECISION,
    CONF_LATEST_VERSION_TEMPLATE,
    CONF_LATEST_VERSION_TOPIC,
    CONF_PAYLOAD_INSTALL,
    CONF_RELEASE_SUMMARY,
    CONF_RELEASE_URL,
    CONF_TITLE,
)
from homeassistant.components.update.const import (
    ATTR_DISPLAY_PRECISION,
    ATTR_INSTALLED_VERSION,
    ATTR_LATEST_VERSION,
    ATTR_RELEASE_SUMMARY,
    ATTR_RELEASE_URL,
    ATTR_TITLE,
    SERVICE_INSTALL,
    UpdateEntityFeature,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_STATE,
    ATTR_SUPPORTED_FEATURES,
    Platform,
)

from ..const import ATTR_ATTRIBUTES, ATTR_INSTALL, COMMAND_INSTALL, CONF_CMD_T
from ..utils import (
    EntityInfo,
    add_config_command,
    build_topic,
    simple_attribute_add,
    validate_message,
)
from .base_entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Update class."""

    PLATFORM = Platform.UPDATE
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a update."""

        if (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES]
            & UpdateEntityFeature.INSTALL
        ):
            add_config_command(config, entity_info, CONF_CMD_T, ATTR_INSTALL)
            config[CONF_PAYLOAD_INSTALL] = COMMAND_INSTALL
        config[CONF_LATEST_VERSION_TOPIC] = build_topic(ATTR_ATTRIBUTES)
        config[CONF_LATEST_VERSION_TEMPLATE] = (
            "{{ value_json['" + ATTR_LATEST_VERSION + "'] }}"
        )

        attributes = entity_info.attributes
        if attributes.get(ATTR_RELEASE_URL):
            config[CONF_RELEASE_URL] = attributes[ATTR_RELEASE_URL]
        if attributes.get(ATTR_RELEASE_SUMMARY):
            config[CONF_RELEASE_SUMMARY] = attributes[ATTR_RELEASE_SUMMARY]
        if attributes.get(ATTR_TITLE):
            config[CONF_TITLE] = attributes[ATTR_TITLE]
        simple_attribute_add(
            config, attributes, CONF_DISPLAY_PRECISION, ATTR_DISPLAY_PRECISION
        )

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a update."""
        await super().async_publish_state(new_state, mybase)
        attributes = new_state.attributes
        await mqtt.async_publish(
            self._hass,
            f"{mybase}{ATTR_STATE}",
            attributes[ATTR_INSTALLED_VERSION],
            1,
            self._publish_retain,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a fan."""
        valid, domain, entity, command = validate_message(
            self._hass, msg, DiscoveryItem.PLATFORM
        )
        if not valid:
            return

        entity_id = f"{domain}.{entity}"
        service_payload = {
            ATTR_ENTITY_ID: entity_id,
        }
        if command == COMMAND_INSTALL:
            await self._hass.services.async_call(
                domain, SERVICE_INSTALL, service_payload
            )
