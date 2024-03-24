"""Schema for MQTT Discovery Stream."""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.mqtt import valid_publish_topic
from homeassistant.helpers.entityfilter import INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA

from .const import (
    CONF_BASE_TOPIC,
    CONF_BIRTH_TOPIC,
    CONF_COMMAND_TOPIC,
    CONF_DISCOVERY_TOPIC,
    CONF_PUBLISH_ATTRIBUTES,
    CONF_PUBLISH_DISCOVERY,
    CONF_PUBLISH_RETAIN,
    CONF_PUBLISH_TIMESTAMPS,
    CONF_REPUBLISH_TIME,
    DEFAULT_LOOP_TIME,
    DEFAULT_RETAIN,
    DOMAIN,
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA.extend(
            {
                vol.Required(CONF_BASE_TOPIC): valid_publish_topic,
                vol.Optional(CONF_DISCOVERY_TOPIC): vol.Any(valid_publish_topic, None),
                vol.Optional(CONF_COMMAND_TOPIC): vol.Any(valid_publish_topic, None),
                vol.Optional(CONF_BIRTH_TOPIC): vol.Any(valid_publish_topic, None),
                vol.Optional(CONF_PUBLISH_ATTRIBUTES, default=False): cv.boolean,
                vol.Optional(CONF_PUBLISH_TIMESTAMPS, default=False): cv.boolean,
                vol.Optional(CONF_PUBLISH_DISCOVERY, default=False): cv.boolean,
                vol.Optional(CONF_PUBLISH_RETAIN, default=DEFAULT_RETAIN): cv.boolean,
                vol.Optional(
                    CONF_REPUBLISH_TIME, default=DEFAULT_LOOP_TIME
                ): cv.time_period,
            }
        ),
    },
    extra=vol.ALLOW_EXTRA,
)
