"""light methods for MQTT Discovery Statestream."""
import json
import logging

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_HS_COLOR,
    ATTR_RGB_COLOR,
    ATTR_TRANSITION,
    ATTR_XY_COLOR,
    SUPPORT_BRIGHTNESS,
    SUPPORT_EFFECT,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
)
from homeassistant.helpers.entity import get_supported_features
from homeassistant.helpers.json import JSONEncoder

from ..const import ATTR_B, ATTR_COLOR, ATTR_G, ATTR_H, ATTR_R, ATTR_S, ATTR_X, ATTR_Y

_LOGGER = logging.getLogger(__name__)


class Light:
    """Light class."""

    def __init__(self, hass):
        """Initialise the light class."""
        self._hass = hass

    def build_config(self, config, entity_id, new_state, mybase):
        """Build the config for a light."""
        del config["json_attr_t"]
        config["cmd_t"] = f"{mybase}set_light"
        config["schema"] = "json"

        supported_features = get_supported_features(self._hass, entity_id)
        if supported_features & SUPPORT_BRIGHTNESS:
            config["brightness"] = True
        if supported_features & SUPPORT_EFFECT:
            config["effect"] = True
        if "supported_color_modes" in new_state.attributes:
            config["color_mode"] = True
            config["supported_color_modes"] = new_state.attributes[
                "supported_color_modes"
            ]

    def build_state(self, new_state):
        """Build the state for a light."""
        payload = {
            "state": "ON" if new_state.state == STATE_ON else "OFF",
        }
        if "brightness" in new_state.attributes:
            payload["brightness"] = new_state.attributes["brightness"]
        if "color_mode" in new_state.attributes:
            payload["color_mode"] = new_state.attributes["color_mode"]
        if "color_temp" in new_state.attributes:
            payload["color_temp"] = new_state.attributes["color_temp"]
        if "effect" in new_state.attributes:
            payload["effect"] = new_state.attributes["effect"]

        color = {}
        if "hs_color" in new_state.attributes:
            color["h"] = new_state.attributes["hs_color"][0]
            color["s"] = new_state.attributes["hs_color"][1]
        if "xy_color" in new_state.attributes:
            color["x"] = new_state.attributes["xy_color"][0]
            color["x"] = new_state.attributes["xy_color"][1]
        if "rgb_color" in new_state.attributes:
            color["r"] = new_state.attributes["rgb_color"][0]
            color["g"] = new_state.attributes["rgb_color"][1]
            color["b"] = new_state.attributes["rgb_color"][2]
        if color:
            payload["color"] = color

        return json.dumps(payload, cls=JSONEncoder)

    async def async_handle_message(self, domain, entity, msg):
        """Handle a message for a light."""
        payload_json = json.loads(msg.payload)
        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        if ATTR_TRANSITION in payload_json:
            service_payload[ATTR_TRANSITION] = payload_json[ATTR_TRANSITION]

        if payload_json["state"] == "ON":
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
            await self._hass.services.async_call(
                domain, SERVICE_TURN_ON, service_payload
            )
        elif payload_json["state"] == "OFF":
            await self._hass.services.async_call(
                domain, SERVICE_TURN_OFF, service_payload
            )
        else:
            _LOGGER.error(
                'Invalid state for "set_light" - payload: %s for %s',
                {msg.payload},
                {entity},
            )
