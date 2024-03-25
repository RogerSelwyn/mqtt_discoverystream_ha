[![Validate with hassfest](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hassfest.yaml/badge.svg)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hassfest.yaml) [![HACS Validate](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hacs.yaml/badge.svg)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/actions/workflows/validate_hacs.yaml) [![CodeFactor](https://www.codefactor.io/repository/github/rogerselwyn/mqtt_discoverystream_ha/badge)](https://www.codefactor.io/repository/github/rogerselwyn/mqtt_discoverystream_ha) [![Downloads for latest release](https://img.shields.io/github/downloads/RogerSelwyn/mqtt_discoverystream_ha/latest/total.svg)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/releases/latest)

![GitHub release](https://img.shields.io/github/v/release/RogerSelwyn/mqtt_discoverystream_ha) [![maintained](https://img.shields.io/maintenance/yes/2024.svg)](#) [![maintainer](https://img.shields.io/badge/maintainer-%20%40RogerSelwyn-blue.svg)](https://github.com/RogerSelwyn) [![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration) 

### This is a very substantial re-write of the version by @koying which adds Climate and Cover support as well as providing a couple of fixes. It is available to be merged back if desired.

# MQTT DiscoveryStream integration for Home Assistant

This is an "extension" of the builtin [`mqtt_statestream`](https://www.home-assistant.io/integrations/mqtt_statestream/) integration.  
Besides the functionalities of the hereabove, it also allows to publish and handles an [MQTT "discovery"](https://www.home-assistant.io/docs/mqtt/discovery) setup.

## Supported entities
Provides discovery support for:
- Binary Sensor
- Climate
- Cover
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

This integration can only be configured via YAML.
The base options are the same as the mqtt_statestream one. 

| key                | default | required | description                                                                        |
| ------------------ | ------- | -------- | ---------------------------------------------------------------------------------- |
| base_topic         | none    | yes      | Base topic used to generate the actual topic used to publish.                      |
| discovery_topic    | --->    | no       | Topic where the configuration topics will be created. Defaults to base_topic       |
| command_topic      | --->    | no       | Topic where any command responses will be created. Defaults to base_topic          |
| publish_attributes | false   | no       | Publish attributes of the entity as well as the state.                             |
| publish_timestamps | false   | no       | Publish the last_changed and last_updated timestamps for the entity.               |
| publish_discovery  | false   | no       | Publish the discovery topic ("config").                                            |
| publish_retain     | false   | no       | When set to true publishes messages with retain bit turned on.                     |
| republish_time     | 5 mins  | no       | Sets the time between iterations of republishing discovery/state for all entities. |
| include / exclude  | none    | no       | Configure which integrations should be included / excluded from publishing.        |
| local_status       | none    | no       | See below                                                                          |
| remote_status      | none    | no       | See below                                                                          |


#### local_status

In order for the remote HA instance to be informed when the local HA instance goes offline (and therefore its entities are unavailable), the local HA status needs to be available at the remote broker. By default, at the local end it is located at `homeassistant/status`, which users will likely rewrite to a different location on the remote broker.

| key                | default | required | description                                                                        |
| ------------------ | ------- | -------- | ---------------------------------------------------------------------------------- |
| topic              | none    | no       | Topic at the slave for master's HA status. Defaults to base_topic + `/status`.     |
| online_status      | online  | no       | As configured in MQTT integration for master's HA online status.                   |
| offline_status     | offline | no       | As configured in MQTT integration for master's HA offline status.                  |

```yaml
  local_status:
    topic: master/status
    online_status: online
    offline_status: offline
```


#### remote_status

In order for the master HA instance to be informed when the remote HA instance has come online (and therefore that it should resend discovery information), the remote HA status needs to be available at the local broker. By default, at the remote end it is located at `homeassistant/status`, which users will likely rewrite to a different location on the local broker.

| key                | default | required | description                                                                        |
| ------------------ | ------- | -------- | ---------------------------------------------------------------------------------- |
| topic              | none    | no       | Topic at the master for slave's HA status. Defaults to base_topic + `/status`.     |
| online_status      | online  | no       | As configured in MQTT integration for slave's HA online status.                    |

```yaml
  remote_status:
    topic: master/status
    online_status: online
```

## Services

A service called `publish_discovery_state` is provided when `publish_discovery` is enabled in the configuration. The service triggers a re-publication of the discovery and current state information for each entity that matches the inclusion/exclusion filter. There are no attributes/parameters for the service.

## Topic Handling

* Discovery messages will be published to the `discovery_topic` when `publish_discovery` is enabled. 
* State messages will be sent to the `base_topic`.
* Commands from entities at the slave site will be subscribed to on the `command_topic`.
* Birth messages from the slave site will be subscribed to on the `birth_topic`, which must end in `/status`. `/status` will be added to the topic if missing. 

## Discovery of entities and Publication of states

Discovery and state messages will be published under 4 situations:
1. Completion of Home Assistant startup
1. Connection of slave broker and receipt of `online` message at the `birth_topic`
1. Initiation of `publish_discovery_state` service
1. First change of state of an entity, where none of the first 3 items has occurred 

## Flowchart

### Startup
```mermaid
sequenceDiagram
participant H as Home Assistant Master
participant M as Master Broker
participant S as Slave Broker
participant R as Home Assistant Slave
opt
  H->>+M: Entity changed state
  M->>S: Publish discovery<br/>(discovery_topic)
  S->>R: Create entity
  M->>S: Publish state<br/>(base_topic)
  S->>R: Set state
  M->>-H: End
end
H->>+M: Home Assistant Started
loop 
  M->>S: Publish discovery<br/>(discovery_topic)
  S->>R: Create entity
  M->>S: Publish state<br/>(base_topic)
  S->>R: Set state
end
M->>-H: End
```

### Running
```mermaid
sequenceDiagram
participant H as Home Assistant Master
participant M as Master Broker
participant S as Slave Broker
participant R as Home Assistant Slave
opt
  H->>+M: Entity changed state
  M->>S: Publish state<br/>(base_topic)
  S->>R: Set state
  M->>-H: End
end

opt
  R->>S: Home Assistant Started
  S->>+M: Publish birth<br/>(birth_topic)
  loop 
    M->>S: Publish discovery<br/>(discovery_topic)
    S->>R: Create entity
  end
note right of M: Wait 5 seconds
  loop 
    M->>S: Publish state<br/>(base_topic)
    S->>R: Set state
  end
  M->>-S: End
end
opt
  R->>S: Command initiated
  S->>M: Publish command<br/>(command_topic)
  M->>H: Perform command on entity
  H->>+M: Entity changed state
  M->>S: Publish state<br/>(base_topic)
  S->>R: Set state
end

opt
  H->>+M: Service request
  loop
    M->>S: Publish discovery<br/>(discovery_topic)
    S->>R: Create entity
    M->>S: Publish state<br/>(base_topic)
    S->>R: Set state
  end
  M->>-H: End
end
```


## Credits

- This custom component is based upon the `mqtt_statestream` one from HA Core.  
