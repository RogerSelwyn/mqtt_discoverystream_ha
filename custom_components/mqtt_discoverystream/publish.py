"""Publishiong discovery for MQTT Discovery Stream."""
from homeassistant.components.light import SUPPORT_BRIGHTNESS, SUPPORT_EFFECT
from homeassistant.const import STATE_OFF, STATE_ON, STATE_OPEN, STATE_CLOSED
from homeassistant.helpers.entity import get_supported_features


async def async_publish_discovery(hass, has_includes, mybase, new_state, entity_id):

    ent_parts = entity_id.split(".")
    ent_domain = ent_parts[0]
    ent_id = ent_parts[1]
    config = {
        "uniq_id": f"mqtt_{entity_id}",
        "name": ent_id.replace("_", " ").title(),
        "stat_t": f"{mybase}state",
        "json_attr_t": f"{mybase}attributes",
        "avty_t": f"{mybase}availability",
    }
    if "device_class" in new_state.attributes:
        config["dev_cla"] = new_state.attributes["device_class"]
    if "unit_of_measurement" in new_state.attributes:
        config["unit_of_meas"] = new_state.attributes["unit_of_measurement"]
    if "state_class" in new_state.attributes:
        config["stat_cla"] = new_state.attributes["state_class"]

    publish_config = False
    if ent_domain == "sensor" and (
        has_includes or "device_class" in new_state.attributes
    ):
        publish_config = True

    elif ent_domain == "binary_sensor" and (
        has_includes or "device_class" in new_state.attributes
    ):
        config["pl_off"] = STATE_OFF
        config["pl_on"] = STATE_ON
        publish_config = True

    elif ent_domain == "switch":
        config["pl_off"] = STATE_OFF
        config["pl_on"] = STATE_ON
        config["cmd_t"] = f"{mybase}set"
        publish_config = True

    elif ent_domain == "cover":
        config["pl_closed"] = STATE_CLOSED
        config["pl_open"] = STATE_OPEN
        config["cmd_t"] = f"{mybase}set"
        publish_config = True

    elif ent_domain == "device_tracker":
        publish_config = True

    elif ent_domain == "climate":
        config["current_temperature_topic"] = f"{mybase}attributes"
        config["current_temperature_template"] = "{{ value_json.current_temperature }}"
        if "icon" in new_state.attributes:
            config["icon"] = new_state.attributes["icon"]
        config["max_temp"] = new_state.attributes["max_temp"]
        config["min_temp"] = new_state.attributes["min_temp"]
        config["modes"] = new_state.attributes["hvac_modes"]
        config["mode_state_topic"] = f"{mybase}state"
        preset_modes = new_state.attributes["preset_modes"]
        if "none" in preset_modes:
            preset_modes.remove("none")
        config["preset_modes"] = preset_modes
        config["preset_mode_command_topic"] = f"{mybase}preset_command"
        config["preset_mode_state_topic"] = f"{mybase}attributes"
        config["preset_mode_value_template"] = "{{ value_json.preset_mode }}"
        config["temperature_state_topic"] = f"{mybase}attributes"
        config["temperature_state_template"] = "{{ value_json.temperature }}"
        publish_config = True

    elif ent_domain == "light":
        del config["json_attr_t"]
        config["cmd_t"] = f"{mybase}set_light"
        config["schema"] = "json"

        supported_features = get_supported_features(hass, entity_id)
        if supported_features & SUPPORT_BRIGHTNESS:
            config["brightness"] = True
        if supported_features & SUPPORT_EFFECT:
            config["effect"] = True
        if "supported_color_modes" in new_state.attributes:
            config["color_mode"] = True
            config["supported_color_modes"] = new_state.attributes[
                "supported_color_modes"
            ]

        publish_config = True

    if publish_config:
        for entry in ent_reg.entities.values():
            if entry.entity_id != entity_id:
                continue
            for device in dev_reg.devices.values():
                if device.id != entry.device_id:
                    continue
                config["dev"] = {}
                if device.manufacturer:
                    config["dev"]["mf"] = device.manufacturer
                if device.model:
                    config["dev"]["mdl"] = device.model
                if device.name:
                    config["dev"]["name"] = device.name
                if device.sw_version:
                    config["dev"]["sw"] = device.sw_version
                if device.identifiers:
                    config["dev"]["ids"] = [id[1] for id in device.identifiers]
                if device.connections:
                    config["dev"]["cns"] = device.connections

        encoded = json.dumps(config, cls=JSONEncoder)
        entity_disc_topic = f"{discovery_topic}{entity_id.replace('.', '/')}/config"
        await mqtt.async_publish(entity_disc_topic, encoded, 1, True)
        hass.data[DOMAIN][discovery_topic]["conf_published"].append(entity_id)
