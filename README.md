[![Validate with hassfest](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hassfest.yaml/badge.svg)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hassfest.yaml) [![HACS Action](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hacs.yaml/badge.svg)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hacs.yaml) [![Downloads for latest release](https://img.shields.io/github/downloads/RogerSelwyn/mqtt_discoverystream_ha/latest/total.svg)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/releases/latest)

![GitHub release](https://img.shields.io/github/v/release/RogerSelwyn/mqtt_discoverystream_ha) [![maintained](https://img.shields.io/maintenance/yes/2023.svg)](#) [![maintainer](https://img.shields.io/badge/maintainer-%20%40RogerSelwyn-blue.svg)](https://github.com/RogerSelwyn) [![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration) 

# This is a fork of the version by @koying which adds Climate and provides a couple of fixes. It is intended to be merged back to that version.

# MQTT DiscoveryStream integration for Home Assistant

This is an "extension" of the builtin [`mqtt_statestream`](https://www.home-assistant.io/integrations/mqtt_statestream/) integration.  
Besides the functionalities of the hereabove, it also allows to publish and handles an [MQTT "discovery"](https://www.home-assistant.io/docs/mqtt/discovery) setup.

## Supported entities
Provides discovery support for:
- Binary Sensor
- Climate
- Light
- Sensor
- Switch

## Pre-requisites

1. MQTT configured

## Installation

### HACS

1. Launch HACS
1. Navigate to the Integrations section
1. Add this repository as an Custom Repository (Integration) via the menu at top right (Only required if you wish to use this forked version).
1. Search for "MQTT DiscoveryStream"
1. Select "Install this repository"
1. Restart Home Assistant

### Home Assistant

The integration is configured via YAML only.

Example:

```yaml
mqtt_discoverystream:
  base_topic: test_HA
  publish_attributes: false
  publish_timestamps: true
  publish_discovery: true
  include:
    entities:
      - sensor.owm_hourly_humidity
      - sensor.jellyfin_cloud
      - light.wled_esp
  exclude:
    entities:
      - sensor.plug_xiaomi_1_electrical_measurement
```

## Configuration

### Options

This integration can only be configuration via YAML.
The base options are the same as the mqtt_statestream one. 

| key                | default | required | description                                                                  |
| ------------------ | ------- | -------- | ---------------------------------------------------------------------------- |
| base_topic         | none    | yes      | Base topic used to generate the actual topic used to publish.                |
| discovery_topic    | none    | no       | Topic where the configuration topics will be created. Defaults to base_topic |
| command_topic      | none    | no       | Topic where any command responses will be created. Defaults to base_topic |
| publish_attributes | false   | no       | Publish attributes of the entity as well as the state.                       |
| publish_timestamps | false   | no       | Publish the last_changed and last_updated timestamps for the entity.         |
| publish_discovery  | false   | no       | Publish the discovery topic ("config").                                      |
| include / exclude  | none    | no       | Configure which integrations should be included / excluded from publishing.  |

## Credits

- This custom component is based upon the `mqtt_statestream` one from HA Core.  
