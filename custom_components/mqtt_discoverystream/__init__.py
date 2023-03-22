"""Publish simple item state changes via MQTT."""
import json
import logging

from homeassistant.components import mqtt
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, EVENT_STATE_CHANGED
from homeassistant.core import Event, HomeAssistant, State, callback
from homeassistant.helpers.entityfilter import convert_include_exclude_filter
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.start import async_at_start
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
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, reintroduce-else
    """Set up the MQTT state feed."""
    # Make sure MQTT is available and the entry is loaded
    if not hass.config_entries.async_entries(
        mqtt.DOMAIN
    ) or not await hass.config_entries.async_wait_component(
        hass.config_entries.async_entries(mqtt.DOMAIN)[0]
    ):
        _LOGGER.error("MQTT integration is not available")
        return False

    conf: ConfigType = config[DOMAIN]
    publish_filter = convert_include_exclude_filter(conf)
    base_topic: str = conf.get(CONF_BASE_TOPIC)
    publish_attributes: bool = conf.get(CONF_PUBLISH_ATTRIBUTES)
    publish_timestamps: bool = conf.get(CONF_PUBLISH_TIMESTAMPS)
    if not base_topic.endswith("/"):
        base_topic = f"{base_topic}/"

    publish_discovery = conf.get(CONF_PUBLISH_DISCOVERY)
    if publish_discovery:
        discovery = Discovery(hass, base_topic, conf)

    async def _state_publisher(evt: Event) -> None:
        entity_id: str = evt.data["entity_id"]
        new_state: State = evt.data["new_state"]

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

    @callback
    def _ha_started(hass: HomeAssistant) -> None:
        @callback
        def _event_filter(evt: Event) -> bool:
            entity_id: str = evt.data["entity_id"]
            new_state: State | None = evt.data["new_state"]
            if new_state is None:
                return False
            if not publish_filter(entity_id):
                return False
            return True

        callback_handler = hass.bus.async_listen(
            EVENT_STATE_CHANGED, _state_publisher, _event_filter
        )

        @callback
        def _ha_stopping(_: Event) -> None:
            callback_handler()

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _ha_stopping)

    async_at_start(hass, _ha_started)

    return True
