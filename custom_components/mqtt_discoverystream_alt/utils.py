"""Utilities for MQTT Discovery Stream."""

import logging
from dataclasses import dataclass, field

from homeassistant.components import mqtt

from .const import (
    CONF_BASE_TOPIC,
    CONF_PUBLISHED,
    DOMAIN,
    OUTPUT_ENTITIES,
    SUPPORTED_ENTITY_TYPE_COMMANDS,
)

_LOGGER = logging.getLogger(__name__)


async def async_publish_attribute(
    hass, new_state, mybase, attribute_name, publish_retain, strip=False
):
    """Publish a specific attribute"""
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


def validate_message(hass, msg, platform):
    """Handle a message for a switch."""
    explode_topic = msg.topic.split("/")
    domain = explode_topic[1]
    entity = explode_topic[2]
    command = explode_topic[3]

    # Only handle service calls for discoveries we published
    if f"{domain}.{entity}" not in hass.data[DOMAIN][CONF_PUBLISHED]:
        return False, None, None, None

    if command not in SUPPORTED_ENTITY_TYPE_COMMANDS[platform]:
        command_error(command, msg.payload, entity)
        return False, None, None, None

    _LOGGER.debug("Message received: topic %s; payload: %s", {msg.topic}, {msg.payload})
    return True, domain, entity, command


def translate_entity_type(entity_id):
    """Translate the entity type to the output type."""
    ent_parts = entity_id.split(".")
    if ent_parts[0] in OUTPUT_ENTITIES:
        output_entity = OUTPUT_ENTITIES[ent_parts[0]]
    else:
        output_entity = ent_parts[0]
    return f"{output_entity}.{ent_parts[1]}"


def simple_attribute_add(config, attributes, attribute_name, conf_name=None):
    """Simple check for attribute existence and inclusion."""
    if attribute_name in attributes:
        config[conf_name or attribute_name] = attributes[attribute_name]


def simple_entry_attribute(config_device, attribute, conf_name):
    """Simple check for attribute existence and inclusion."""
    if attribute:
        config_device[conf_name] = attribute


def command_error(command, payload, entity):
    """Log error for invalid command."""
    _LOGGER.error(
        'Invalid service for "%s" - payload: %s for %s',
        command,
        {payload},
        {entity},
    )


@dataclass
class EntityInfo:
    """Information for an entity."""

    mycommand: str = field(init=True, repr=True)
    attributes: str = field(init=True, repr=True)
    mybase: str = field(init=True, repr=True)
    entity_id: str = field(init=True, repr=True)


def add_config_command(config, entity_info: EntityInfo, confname, confvalue):
    """Add relevant commands to discovery config."""
    config[confname] = f"{entity_info.mycommand}/{confvalue}"


def build_topic(attrname):
    """Build a standard topic."""
    return f"~/{attrname}"
