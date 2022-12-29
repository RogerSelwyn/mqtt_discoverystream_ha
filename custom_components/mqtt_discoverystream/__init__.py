"""Publish simple item state changes via MQTT."""
import json
import logging

from homeassistant.components import mqtt
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entityfilter import convert_include_exclude_filter
from homeassistant.helpers.event import async_track_state_change
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_BASE_TOPIC,
    CONF_PUBLISH_ATTRIBUTES,
    CONF_PUBLISH_DISCOVERY,
    CONF_PUBLISH_TIMESTAMPS,
    DOMAIN,
)
from .discovery import Discovery
from .schema import CONFIG_SCHEMA  # noqa: F401

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MQTT state feed."""
    conf = config[DOMAIN]
    publish_filter = convert_include_exclude_filter(conf)
    base_topic = conf.get(CONF_BASE_TOPIC)
    publish_attributes = conf.get(CONF_PUBLISH_ATTRIBUTES)
    publish_timestamps = conf.get(CONF_PUBLISH_TIMESTAMPS)
    if not base_topic.endswith("/"):
        base_topic = f"{base_topic}/"

    publish_discovery = conf.get(CONF_PUBLISH_DISCOVERY)
    if publish_discovery:
        discovery = Discovery(hass, base_topic, conf)

    async def _state_publisher(
        entity_id, old_state, new_state
    ):  # pylint: disable=unused-argument
        if new_state is None:
            return

        if not publish_filter(entity_id):
            return

        mybase = f"{base_topic}{entity_id.replace('.', '/')}/"
        if publish_discovery:
            await discovery.async_state_publish(entity_id, new_state, mybase)
        else:
            payload = new_state.state
            await mqtt.async_publish(hass, f"{mybase}state", payload, 1, True)

        if publish_timestamps:
            if new_state.last_updated:
                await mqtt.async_publish(
                    hass,
                    f"{mybase}last_updated",
                    new_state.last_updated.isoformat(),
                    1,
                    True,
                )
            if new_state.last_changed:
                await mqtt.async_publish(
                    hass,
                    f"{mybase}last_changed",
                    new_state.last_changed.isoformat(),
                    1,
                    True,
                )

        if publish_attributes:
            for key, val in new_state.attributes.items():
                encoded_val = json.dumps(val, cls=JSONEncoder)
                await mqtt.async_publish(hass, mybase + key, encoded_val, 1, True)

    async_track_state_change(hass, MATCH_ALL, _state_publisher)
    return True
