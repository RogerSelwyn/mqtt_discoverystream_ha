"""Schema for MQTT Discovery Stream."""

import probatio

from homeassistant.components.mqtt import valid_publish_topic
from homeassistant.components.mqtt.const import (  # pylint: disable=home-assistant-component-root-import
    AVAILABILITY_LATEST,
    AVAILABILITY_MODES,
    CONF_AVAILABILITY_MODE,
    CONF_TOPIC,
    DEFAULT_PAYLOAD_AVAILABLE,
    DEFAULT_PAYLOAD_NOT_AVAILABLE,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entityfilter import INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA

from .const import (
    CONF_BASE_TOPIC,
    CONF_COMMAND_TOPIC,
    CONF_DISCOVERY_TOPIC,
    CONF_LOCAL_STATUS,
    CONF_OFFLINE_STATUS,
    CONF_ONLINE_STATUS,
    CONF_PUBLISH_ATTRIBUTES,
    CONF_PUBLISH_DISCOVERY,
    CONF_PUBLISH_RETAIN,
    CONF_PUBLISH_TIMESTAMPS,
    CONF_REMOTE_STATUS,
    CONF_REPUBLISH_TIME,
    CONF_RETAIN_DISCOVERY,
    CONF_RETAIN_STATE,
    CONF_STALE_AFTER,
    CONF_UNIQUE_ENTITY_PREFIX,
    CONF_UNIQUE_PREFIX,
    DEFAULT_REFRESH_TIME,
    DEFAULT_RETAIN,
    DOMAIN,
)

LOCAL_STATUS = probatio.Schema(
    {
        probatio.Optional(CONF_TOPIC): probatio.Any(valid_publish_topic, None),
        probatio.Optional(
            CONF_ONLINE_STATUS, default=DEFAULT_PAYLOAD_AVAILABLE
        ): cv.string,
        probatio.Optional(
            CONF_OFFLINE_STATUS, default=DEFAULT_PAYLOAD_NOT_AVAILABLE
        ): cv.string,
    }
)

REMOTE_STATUS = probatio.Schema(
    {
        probatio.Optional(CONF_TOPIC): probatio.Any(valid_publish_topic, None),
        probatio.Optional(
            CONF_ONLINE_STATUS, default=DEFAULT_PAYLOAD_AVAILABLE
        ): cv.string,
    }
)

BASE_SCHEMA = {
    probatio.Required(CONF_BASE_TOPIC): valid_publish_topic,
    probatio.Optional(CONF_DISCOVERY_TOPIC): probatio.Any(valid_publish_topic, None),
    probatio.Optional(CONF_COMMAND_TOPIC): probatio.Any(valid_publish_topic, None),
    probatio.Optional(CONF_REMOTE_STATUS): REMOTE_STATUS,
    probatio.Optional(CONF_LOCAL_STATUS): LOCAL_STATUS,
    probatio.Optional(CONF_PUBLISH_ATTRIBUTES, default=False): cv.boolean,
    probatio.Optional(CONF_PUBLISH_TIMESTAMPS, default=False): cv.boolean,
    probatio.Optional(CONF_PUBLISH_DISCOVERY, default=False): cv.boolean,
    probatio.Optional(CONF_PUBLISH_RETAIN): cv.boolean,
    probatio.Optional(CONF_RETAIN_DISCOVERY, default=DEFAULT_RETAIN): cv.boolean,
    probatio.Optional(CONF_RETAIN_STATE, default=DEFAULT_RETAIN): cv.boolean,
    probatio.Optional(CONF_UNIQUE_PREFIX, default="mqtt"): cv.string,
    probatio.Optional(CONF_UNIQUE_ENTITY_PREFIX): cv.string,
    probatio.Optional(
        CONF_REPUBLISH_TIME, default=DEFAULT_REFRESH_TIME
    ): cv.time_period,
    probatio.Optional(CONF_STALE_AFTER): cv.time_period,
    probatio.Optional(
        CONF_AVAILABILITY_MODE,
        default=AVAILABILITY_LATEST,
    ): probatio.In(AVAILABILITY_MODES),
}


CONFIG_SCHEMA = probatio.Schema(
    {
        DOMAIN: probatio.Schema(
            [INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA.extend(BASE_SCHEMA)],
            "schema_type",
        ),
    },
    extra=probatio.ALLOW_EXTRA,
)
