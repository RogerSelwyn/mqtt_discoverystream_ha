"""Publish simple item state changes via MQTT."""

import asyncio
import logging

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    STARTUP_DELAY,
)
from .mqttunit import MQTTUnit
from .schema import CONFIG_SCHEMA  # noqa: F401

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, reintroduce-else
    """Set up the MQTT state feed."""
    # Make sure MQTT is available and the entry is loaded
    await asyncio.sleep(STARTUP_DELAY)
    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return False

    conf: ConfigType = config[DOMAIN]
    for mqtt_config in conf:
        unit = MQTTUnit(mqtt_config)
        unit.setup_unit(hass)

    return True
