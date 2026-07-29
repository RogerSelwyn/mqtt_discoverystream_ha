"""Tag methods for MQTT Discovery Statestream."""

from homeassistant.components.tag import DOMAIN as TAG_DOMAIN

from .base_entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Tag class."""

    PLATFORM = TAG_DOMAIN
