"""Constants for MQTT Discovery Stream."""

from datetime import timedelta

from homeassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN_DOMAIN
from homeassistant.components.input_button import DOMAIN as INPUT_BUTTON_DOMAIN
from homeassistant.components.input_datetime import DOMAIN as INPUT_DATETIME_DOMAIN
from homeassistant.components.input_number import DOMAIN as INPUT_NUMBER_DOMAIN
from homeassistant.components.input_select import DOMAIN as INPUT_SELECT_DOMAIN
from homeassistant.components.input_text import DOMAIN as INPUT_TEXT_DOMAIN
from homeassistant.components.script import DOMAIN as SCRIPT_DOMAIN
from homeassistant.const import Platform

ATTR_COLOR = "color"  # pylint: disable=invalid-name
ATTR_H = "h"
ATTR_S = "s"
ATTR_X = "x"
ATTR_Y = "y"
ATTR_R = "r"
ATTR_G = "g"
ATTR_B = "b"

ATTR_ATTRIBUTES = "attributes"
ATTR_CODE_DISARM_REQUIRED = "code_disarm_required"
ATTR_CODE_TRIGGER_REQUIRED = "code_trigger_required"
ATTR_COLOR = "color"  # pylint: disable=invalid-name
ATTR_CONFIG = "config"
ATTR_DATETIME = "datetime"
ATTR_INSTALL = "install"
ATTR_JSON = "JSON"
ATTR_MODE = "mode"
ATTR_SUGGESTED_DISPLAY_PRECISION = "suggested_display_precision"

COMMAND_ACTION = "action"
COMMAND_CODE = "code"
COMMAND_DIRECTION = "command_direction"
COMMAND_FAN = "command_fan"
COMMAND_HUMIDITY = "command_humidity"
COMMAND_INSTALL = "install"
COMMAND_MODE = "command_mode"
COMMAND_OSCILLATION = "command_oscillation"
COMMAND_PERCENTAGE = "command_percentage"
COMMAND_PRESET = "command_preset"
COMMAND_SEND = "command_send"
COMMAND_SET = "set"
COMMAND_SET_DATE = "set_date"
COMMAND_SET_DATETIME = "set_datetime"
COMMAND_SET_FAN_SPEED = "set_fan_speed"
COMMAND_SET_LIGHT = "set_light"
COMMAND_SET_POSITION = "set_position"
COMMAND_SET_TILT = "set_tilt"
COMMAND_SET_TIME = "set_time"
COMMAND_SWING = "command_swing"
COMMAND_TEMPERATURE = "command_temperature"


CONF_BASE_TOPIC = "base_topic"
CONF_COMMAND_TOPIC = "command_topic"
CONF_DISCOVERY_TOPIC = "discovery_topic"
CONF_LOCAL_STATUS = "local_status"
CONF_OFFLINE_STATUS = "offline_status"
CONF_ONLINE_STATUS = "online_status"
CONF_PUBLISH_ATTRIBUTES = "publish_attributes"
CONF_PUBLISH_TIMESTAMPS = "publish_timestamps"
CONF_PUBLISH_DISCOVERY = "publish_discovery"
CONF_PUBLISH_RETAIN = "publish_retain"
CONF_REMOTE_STATUS = "remote_status"
CONF_REPUBLISH_TIME = "republish_time"
CONF_UNIQUE_PREFIX = "unique_prefix"

DEFAULT_REFRESH_TIME = timedelta(minutes=5)
DEFAULT_RETAIN = False
DEFAULT_STATE_SLEEP = 1.5

DOMAIN = "mqtt_discoverystream_alt"

STARTUP_DELAY = 0.5

STATE_CAPITAL_ON = "ON"
STATE_CAPITAL_OFF = "OFF"

# These constants are translated via abberviations in mqtt.abbreviations
CONF_AVTY = "avty"
CONF_AVTY_MODE = "avty_mode"
CONF_CMD_T = "cmd_t"
CONF_CMD_TPL = "cmd_tpl"
CONF_COD_ARM_REQ = "cod_arm_req"
CONF_COD_DIS_REQ = "cod_dis_req"
CONF_COD_FORM = "cod_form"
CONF_COD_TRIG_REQ = "cod_trig_req"
CONF_DEF_ENT_ID = "def_ent_id"
CONF_DEV = "dev"
CONF_DEV_CLA = "dev_cla"
CONF_ENT_CAT = "ent_cat"
CONF_ENT_PIC = "ent_pic"
CONF_EVT_TYP = "evt_typ"
CONF_JSON_ATTR_T = "json_attr_t"
CONF_MAX = "max"
CONF_MIN = "min"
CONF_MODE = "mode"
CONF_OPS = "ops"
CONF_PATTERN = "pattern"
CONF_PL_OPEN = "pl_open"
CONF_PL_PRS = "pl_prs"
CONF_SET_POS_T = "set_pos_t"
CONF_STAT_JAM = "stat_jam"
CONF_STAT_LOCKED = "stat_locked"
CONF_STAT_LOCKING = "stat_locking"
CONF_STAT_UNLOCKED = "stat_unlocked"
CONF_STAT_UNLOCKING = "stat_unlocking"
CONF_STAT_T = "stat_t"
CONF_STAT_CLA = "stat_cla"
CONF_STEP = "step"
CONF_SUG_DSP_PRC = "sug_dsp_prc"
CONF_SUP_FEAT = "sup_feat"
CONF_TILDA = "~"
CONF_TILT_CMD_T = "tilt_cmd_t"
CONF_UNIQ_ID = "uniq_id"
CONF_UNIT_OF_MEAS = "unit_of_meas"

CONF_MDL = "mdl"
CONF_MF = "mf"
CONF_SW = "sw"
CONF_IDS = "ids"
CONF_CNS = "cns"
CONF_PL_ON = "pl_on"
CONF_PL_OFF = "pl_off"


SUPPORTED_ENTITY_TYPE_COMMANDS = {
    Platform.ALARM_CONTROL_PANEL: [COMMAND_SET],
    Platform.BINARY_SENSOR: [],
    Platform.BUTTON: [COMMAND_SET],
    Platform.CLIMATE: [
        COMMAND_FAN,
        COMMAND_HUMIDITY,
        COMMAND_MODE,
        COMMAND_SET,
        COMMAND_PRESET,
        COMMAND_SWING,
        COMMAND_TEMPERATURE,
    ],
    Platform.COVER: [COMMAND_SET, COMMAND_SET_POSITION, COMMAND_SET_TILT],
    Platform.DATE: [COMMAND_SET_DATE],
    Platform.DATETIME: [COMMAND_SET_DATETIME],
    Platform.DEVICE_TRACKER: [],
    Platform.EVENT: [],
    Platform.FAN: [
        COMMAND_SET,
        COMMAND_DIRECTION,
        COMMAND_OSCILLATION,
        COMMAND_PERCENTAGE,
        COMMAND_PRESET,
    ],
    Platform.IMAGE: [],
    Platform.LIGHT: [COMMAND_SET_LIGHT],
    Platform.LOCK: [COMMAND_SET],
    Platform.NUMBER: [COMMAND_SET],
    Platform.SCENE: [COMMAND_SET],
    Platform.SELECT: [COMMAND_SET],
    Platform.SENSOR: [],
    Platform.SWITCH: [COMMAND_SET],
    Platform.TEXT: [COMMAND_SET],
    Platform.TIME: [COMMAND_SET_TIME],
    Platform.UPDATE: [COMMAND_INSTALL],
    Platform.VACUUM: [COMMAND_SEND, COMMAND_SET, COMMAND_SET_FAN_SPEED],
    INPUT_BOOLEAN_DOMAIN: [COMMAND_SET],
    INPUT_BUTTON_DOMAIN: [COMMAND_SET],
    INPUT_DATETIME_DOMAIN: [COMMAND_SET_DATETIME, COMMAND_SET_DATE, COMMAND_SET_TIME],
    INPUT_NUMBER_DOMAIN: [COMMAND_SET],
    INPUT_SELECT_DOMAIN: [COMMAND_SET],
    INPUT_TEXT_DOMAIN: [COMMAND_SET],
    SCRIPT_DOMAIN: [COMMAND_SET],
}

# INPUT_DATETIME not included here since it is a special case
# and is translated to datetime, date or time as appropriate
OUTPUT_ENTITIES = {
    INPUT_BOOLEAN_DOMAIN: Platform.SWITCH,
    INPUT_BUTTON_DOMAIN: Platform.BUTTON,
    INPUT_NUMBER_DOMAIN: Platform.NUMBER,
    INPUT_SELECT_DOMAIN: Platform.SELECT,
    INPUT_TEXT_DOMAIN: Platform.TEXT,
    SCRIPT_DOMAIN: Platform.BUTTON,
}

SERVICE_SET_DATETIME = "set_datetime"
