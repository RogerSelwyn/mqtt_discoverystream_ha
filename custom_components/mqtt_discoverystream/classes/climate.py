"""climate methods for MQTT Discovery Statestream."""


class Climate:
    """Climate class."""

    def build_config(self, config, new_state, mybase):
        """Build the config for a climate."""
        config["action_topic"] = f"{mybase}attributes"
        config["action_template"] = "{{ value_json.hvac_action }}"
        config["current_temperature_topic"] = f"{mybase}attributes"
        config["current_temperature_template"] = "{{ value_json.current_temperature }}"
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
