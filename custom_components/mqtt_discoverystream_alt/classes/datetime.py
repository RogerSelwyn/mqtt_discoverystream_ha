"""datetime methods for MQTT Discovery Statestream."""

from homeassistant.const import Platform

from .base_input_entity import DateTimeDiscoveryEntity


class DiscoveryItem(DateTimeDiscoveryEntity):
    """DateTime class."""

    PLATFORM = Platform.DATETIME
