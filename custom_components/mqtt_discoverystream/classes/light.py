"""light methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components import mqtt
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_MODE,
    ATTR_COLOR_TEMP,
    ATTR_EFFECT,
    ATTR_EFFECT_LIST,
    ATTR_HS_COLOR,
    ATTR_RGB_COLOR,
    ATTR_SUPPORTED_COLOR_MODES,
    ATTR_TRANSITION,
    ATTR_XY_COLOR,
    SUPPORT_BRIGHTNESS,
    SUPPORT_EFFECT,
)
from homeassistant.components.mqtt.const import CONF_SCHEMA
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_STATE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
    Platform,
)
from homeassistant.helpers.entity import get_supported_features
from homeassistant.helpers.json import JSONEncoder

from ..const import (
    ATTR_B,
    ATTR_COLOR,
    ATTR_G,
    ATTR_H,
    ATTR_JSON,
    ATTR_R,
    ATTR_S,
    ATTR_SET_LIGHT,
    ATTR_X,
    ATTR_Y,
    CONF_CMD_T,
    CONF_JSON_ATTR_T,
    CONF_PUBLISHED,
    DOMAIN,
    STATE_CAPITAL_OFF,
    STATE_CAPITAL_ON,
)
from ..utils import EntityInfo
from .entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class Light(DiscoveryEntity):
    """Light class."""

    def build_config(self, config, entity_info: EntityInfo):  # noqa: F821
        """Build the config for a light."""
        del config[CONF_JSON_ATTR_T]
        config[CONF_CMD_T] = f"{entity_info.mycommand}{ATTR_SET_LIGHT}"
        config[CONF_SCHEMA] = ATTR_JSON

        supported_features = get_supported_features(self._hass, entity_info.entity_id)
        if (supported_features & SUPPORT_BRIGHTNESS) or (
            ATTR_BRIGHTNESS in entity_info.attributes
        ):
            config[ATTR_BRIGHTNESS] = True
        if supported_features & SUPPORT_EFFECT:
            config[ATTR_EFFECT] = True
            config[ATTR_EFFECT_LIST] = entity_info.attributes[ATTR_EFFECT_LIST]
        if ATTR_SUPPORTED_COLOR_MODES in entity_info.attributes:
            config[ATTR_SUPPORTED_COLOR_MODES] = entity_info.attributes[
                ATTR_SUPPORTED_COLOR_MODES
            ]
            config[ATTR_BRIGHTNESS] = True
        else:
            config[ATTR_COLOR_MODE] = False
            _LOGGER.warning(
                "Light '%s' has no '%s' attribute which is mandatory. Please report to owner.",
                entity_info.entity_id,
                ATTR_SUPPORTED_COLOR_MODES,
            )

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a light."""
        payload = {
            ATTR_STATE: STATE_CAPITAL_ON
            if new_state.state == STATE_ON
            else STATE_CAPITAL_OFF,
        }
        self._add_attribute(payload, new_state, ATTR_BRIGHTNESS)
        self._add_attribute(payload, new_state, ATTR_COLOR_MODE)
        self._add_attribute(payload, new_state, ATTR_COLOR_TEMP)
        self._add_attribute(payload, new_state, ATTR_EFFECT)
        self._add_attribute(payload, new_state, ATTR_BRIGHTNESS)
        self._add_attribute(payload, new_state, ATTR_BRIGHTNESS)

        if color := self._add_colors(new_state):
            payload[ATTR_COLOR] = color

        payload = json.dumps(payload, cls=JSONEncoder)
        await mqtt.async_publish(
            self._hass, f"{mybase}{ATTR_STATE}", payload, 1, self._publish_retain
        )

    def _add_attribute(self, payload, new_state, attribute):
        if attribute in new_state.attributes and new_state.attributes[attribute]:
            payload[attribute] = new_state.attributes[attribute]

    def _add_colors(self, new_state):
        color = {}
        if (
            ATTR_HS_COLOR in new_state.attributes
            and new_state.attributes[ATTR_HS_COLOR]
        ):
            color[ATTR_H] = new_state.attributes[ATTR_HS_COLOR][0]
            color[ATTR_S] = new_state.attributes[ATTR_HS_COLOR][1]
        if (
            ATTR_XY_COLOR in new_state.attributes
            and new_state.attributes[ATTR_XY_COLOR]
        ):
            color[ATTR_X] = new_state.attributes[ATTR_XY_COLOR][0]
            color[ATTR_Y] = new_state.attributes[ATTR_XY_COLOR][1]
        if (
            ATTR_RGB_COLOR in new_state.attributes
            and new_state.attributes[ATTR_RGB_COLOR]
        ):
            color[ATTR_R] = new_state.attributes[ATTR_RGB_COLOR][0]
            color[ATTR_G] = new_state.attributes[ATTR_RGB_COLOR][1]
            color[ATTR_B] = new_state.attributes[ATTR_RGB_COLOR][2]

        return color

    async def async_subscribe(self, command_topic):
        """Subscribe to messages for a light."""
        await mqtt.async_subscribe(
            self._hass,
            f"{command_topic}{Platform.LIGHT}/+/{ATTR_SET_LIGHT}",
            self._async_handle_message,
        )
        return True

    async def _async_handle_message(self, msg):
        """Handle a message for a light."""
        explode_topic = msg.topic.split("/")
        domain = explode_topic[1]
        entity = explode_topic[2]

        # Only handle service calls for discoveries we published
        if f"{domain}.{entity}" not in self._hass.data[DOMAIN][CONF_PUBLISHED]:
            return

        _LOGGER.debug(
            "Message received: topic %s; payload: %s", {msg.topic}, {msg.payload}
        )

        payload_json = json.loads(msg.payload)
        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        if ATTR_TRANSITION in payload_json:
            service_payload[ATTR_TRANSITION] = payload_json[ATTR_TRANSITION]

        if payload_json[ATTR_STATE] == STATE_CAPITAL_ON:
            if ATTR_BRIGHTNESS in payload_json:
                service_payload[ATTR_BRIGHTNESS] = payload_json[ATTR_BRIGHTNESS]
            if ATTR_COLOR_TEMP in payload_json:
                service_payload[ATTR_COLOR_TEMP] = payload_json[ATTR_COLOR_TEMP]
            if ATTR_COLOR in payload_json:
                if ATTR_H in payload_json[ATTR_COLOR]:
                    service_payload[ATTR_HS_COLOR] = [
                        payload_json[ATTR_COLOR][ATTR_H],
                        payload_json[ATTR_COLOR][ATTR_S],
                    ]
                if ATTR_X in payload_json[ATTR_COLOR]:
                    service_payload[ATTR_XY_COLOR] = [
                        payload_json[ATTR_COLOR][ATTR_X],
                        payload_json[ATTR_COLOR][ATTR_Y],
                    ]
                if ATTR_R in payload_json[ATTR_COLOR]:
                    service_payload[ATTR_RGB_COLOR] = [
                        payload_json[ATTR_COLOR][ATTR_R],
                        payload_json[ATTR_COLOR][ATTR_G],
                        payload_json[ATTR_COLOR][ATTR_B],
                    ]
            if ATTR_EFFECT in payload_json:
                service_payload[ATTR_EFFECT] = payload_json[ATTR_EFFECT]
            await self._hass.services.async_call(
                domain, SERVICE_TURN_ON, service_payload
            )
        elif payload_json[ATTR_STATE] == STATE_CAPITAL_OFF:
            await self._hass.services.async_call(
                domain, SERVICE_TURN_OFF, service_payload
            )
        else:
            _LOGGER.error(
                'Invalid state for "%s" - payload: %s for %s',
                ATTR_SET_LIGHT,
                {msg.payload},
                {entity},
            )
