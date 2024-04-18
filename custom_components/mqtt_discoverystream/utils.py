"""Utilities for MQTT Discovery Stream."""

import json
from dataclasses import dataclass, field

from homeassistant.components import mqtt
from homeassistant.const import ATTR_STATE
from homeassistant.helpers.json import JSONEncoder

from .const import ATTR_ATTRIBUTES, CONF_BASE_TOPIC


async def async_publish_base_attributes(
    hass, new_state, mybase, publish_retain, publish_state=True
):
    """Publish the basic attributes for the entity state."""
    if publish_state:
        await mqtt.async_publish(
            hass, f"{mybase}{ATTR_STATE}", new_state.state, 1, publish_retain
        )

    attributes = dict(new_state.attributes.items())
    encoded = json.dumps(attributes, cls=JSONEncoder)
    await mqtt.async_publish(
        hass, f"{mybase}{ATTR_ATTRIBUTES}", encoded, 1, publish_retain
    )


async def async_publish_attribute(
    hass, new_state, mybase, attribute_name, publish_retain, strip=False
):
    """Publish a s[ecific attribute"""
    if attribute_name in new_state.attributes:
        value = new_state.attributes[attribute_name]
        if value and strip:
            value = value.strip('"')
        await mqtt.async_publish(
            hass,
            f"{mybase}{attribute_name}",
            value,
            1,
            publish_retain,
        )


def set_topic(conf, topic):
    """Create the topic string."""
    response_topic = conf.get(topic) or conf.get(CONF_BASE_TOPIC)
    if not response_topic.endswith("/"):
        response_topic = f"{response_topic}/"
    return response_topic


@dataclass
class EntityInfo:
    """Information for an entity."""

    mycommand: str = field(init=True, repr=True)
    attributes: str = field(init=True, repr=True)
    mybase: str = field(init=True, repr=True)
    entity_id: str = field(init=True, repr=True)
