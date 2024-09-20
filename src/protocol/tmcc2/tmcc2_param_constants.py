import abc
from enum import verify, UNIQUE, IntEnum

from src.protocol.command_def import Mixins, CommandDefEnum
from src.protocol.tmcc2.tmcc2_constants import TMCC2Enum, TMCC2CommandDef, TMCC2CommandPrefix
from src.protocol.tmcc2.tmcc2_constants import TMCC2_SOUND_OFF_COMMAND, TMCC2_SOUND_ON_COMMAND

"""
    Legacy/TMCC2 Multi-byte Command sequences
"""


class TMCC2ParameterEnum(TMCC2Enum):
    """
        Marker Interface for all TMCC2 enums
    """
    pass


"""
    Word #1 - Parameter indexes
"""
TMCC2_PARAMETER_INDEX_PREFIX: int = 0x70
TMCC2_PARAMETER_ASSIGNMENT_PARAMETER_INDEX: int = 0x01
TMCC2_RAIL_SOUNDS_DIALOG_TRIGGERS_PARAMETER_INDEX: int = 0x02
TMCC2_RAIL_SOUNDS_EFFECTS_TRIGGERS_PARAMETER_INDEX: int = 0x04
TMCC2_RAIL_SOUNDS_MASKING_CONTROL_PARAMETER_INDEX: int = 0x06
TMCC2_EFFECTS_CONTROLS_PARAMETER_INDEX: int = 0x0C
TMCC2_LIGHTING_CONTROLS_PARAMETER_INDEX: int = 0x0D
TMCC2_VARIABLE_LENGTH_COMMAND_PARAMETER_INDEX: int = 0x0F


@verify(UNIQUE)
class TMCC2ParameterIndex(Mixins, IntEnum):
    PARAMETER_ASSIGNMENT = TMCC2_PARAMETER_ASSIGNMENT_PARAMETER_INDEX
    DIALOG_TRIGGERS = TMCC2_RAIL_SOUNDS_DIALOG_TRIGGERS_PARAMETER_INDEX
    EFFECTS_TRIGGERS = TMCC2_RAIL_SOUNDS_EFFECTS_TRIGGERS_PARAMETER_INDEX
    MASKING_CONTROL = TMCC2_RAIL_SOUNDS_MASKING_CONTROL_PARAMETER_INDEX
    EFFECTS_CONTROLS = TMCC2_EFFECTS_CONTROLS_PARAMETER_INDEX
    LIGHTING_CONTROLS = TMCC2_LIGHTING_CONTROLS_PARAMETER_INDEX
    VARIABLE_LENGTH_COMMAND = TMCC2_VARIABLE_LENGTH_COMMAND_PARAMETER_INDEX


class TMCC2ParameterCommandDef(TMCC2CommandDef):
    __metaclass__ = abc.ABCMeta

    def __init__(self, command_bits: int) -> None:
        super().__init__(command_bits)
        self._first_byte = TMCC2CommandPrefix.ENGINE


class TMCC2ParameterData(CommandDefEnum):
    """
        Marker interface for all Parameter Data enums
    """
    pass


"""
    Word #2 - RailSounds Dialog trigger controls (index 0x2)
"""
TMCC2_DIALOG_CONTROL_CONVENTIONAL_SHUTDOWN: int = 0x01
TMCC2_DIALOG_CONTROL_SCENE_TWO: int = 0x02
TMCC2_DIALOG_CONTROL_SCENE_SEVEN: int = 0x03
TMCC2_DIALOG_CONTROL_SCENE_FIVE: int = 0x04
TMCC2_DIALOG_CONTROL_SHORT_HORN: int = 0x05
TMCC2_DIALOG_CONTROL_TOWER_ENGINE_STARTUP: int = 0x06
TMCC2_DIALOG_CONTROL_ENGINEER_DEPARTURE_DENIED: int = 0x07
TMCC2_DIALOG_CONTROL_ENGINEER_DEPARTURE_GRANTED: int = 0x08
TMCC2_DIALOG_CONTROL_ENGINEER_HAVE_DEPARTED: int = 0x09
TMCC2_DIALOG_CONTROL_ENGINEER_ALL_CLEAR: int = 0x0A
TMCC2_DIALOG_CONTROL_TOWER_STOP_HOLD: int = 0x0B
TMCC2_DIALOG_CONTROL_TOWER_RESTRICTED_SPEED: int = 0x0C
TMCC2_DIALOG_CONTROL_TOWER_SLOW_SPEED: int = 0x0D
TMCC2_DIALOG_CONTROL_TOWER_MEDIUM_SPEED: int = 0x0E
TMCC2_DIALOG_CONTROL_TOWER_LIMITED_SPEED: int = 0x0F
TMCC2_DIALOG_CONTROL_TOWER_NORMAL_SPEED: int = 0x10
TMCC2_DIALOG_CONTROL_TOWER_HIGHBALL_SPEED: int = 0x11
TMCC2_DIALOG_CONTROL_ENGINEER_ARRIVING_SOON: int = 0x12
TMCC2_DIALOG_CONTROL_ENGINEER_HAVE_ARRIVED: int = 0x13
TMCC2_DIALOG_CONTROL_ENGINEER_SHUTDOWN: int = 0x14
TMCC2_DIALOG_CONTROL_ENGINEER_ID: int = 0x15
TMCC2_DIALOG_CONTROL_ENGINEER_ACK: int = 0x16
TMCC2_DIALOG_CONTROL_ENGINEER_STOP_SPEED_ACK: int = 0x17
TMCC2_DIALOG_CONTROL_ENGINEER_RESTRICTED_SPEED_ACK: int = 0x18
TMCC2_DIALOG_CONTROL_ENGINEER_SLOW_SPEED_ACK: int = 0x19
TMCC2_DIALOG_CONTROL_ENGINEER_MEDIUM_SPEED_ACK: int = 0x1A
TMCC2_DIALOG_CONTROL_ENGINEER_LIMITED_SPEED_ACK: int = 0x1B
TMCC2_DIALOG_CONTROL_ENGINEER_NORMAL_SPEED_ACK: int = 0x1C
TMCC2_DIALOG_CONTROL_ENGINEER_HIGHBALL_SPEED_ACK: int = 0x1D


@verify(UNIQUE)
class TMCC2RailSoundsDialogControl(TMCC2ParameterEnum):
    CONVENTIONAL_SHUTDOWN = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_CONVENTIONAL_SHUTDOWN)
    SCENE_TWO = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_SCENE_TWO)
    SCENE_FIVE = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_SCENE_FIVE)
    SCENE_SEVEN = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_SCENE_SEVEN)
    SHORT_HORN = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_SHORT_HORN)
    TOWER_STARTUP = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_ENGINE_STARTUP)
    ENGINEER_DEPARTURE_DENIED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_DEPARTURE_DENIED)
    ENGINEER_DEPARTURE_GRANTED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_DEPARTURE_GRANTED)
    ENGINEER_HAVE_DEPARTED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_HAVE_DEPARTED)
    ENGINEER_ALL_CLEAR = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_ALL_CLEAR)
    TOWER_SPEED_STOP_HOLD = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_STOP_HOLD)
    TOWER_SPEED_RESTRICTED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_RESTRICTED_SPEED)
    TOWER_SPEED_SLOW = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_SLOW_SPEED)
    TOWER_SPEED_MEDIUM = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_MEDIUM_SPEED)
    TOWER_SPEED_LIMITED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_LIMITED_SPEED)
    TOWER_SPEED_NORMAL = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_NORMAL_SPEED)
    TOWER_SPEED_HIGHBALL = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_TOWER_HIGHBALL_SPEED)
    ENGINEER_ARRIVING_SOON = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_ARRIVING_SOON)
    ENGINEER_HAVE_ARRIVED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_HAVE_ARRIVED)
    ENGINEER_SHUTDOWN = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_SHUTDOWN)
    ENGINEER_ID = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_ID)
    ENGINEER_ACK = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_ACK)
    ENGINEER_SPEED_STOP_HOLD = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_STOP_SPEED_ACK)
    ENGINEER_SPEED_RESTRICTED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_RESTRICTED_SPEED_ACK)
    ENGINEER_SPEED_SLOW = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_SLOW_SPEED_ACK)
    ENGINEER_SPEED_MEDIUM = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_MEDIUM_SPEED_ACK)
    ENGINEER_SPEED_LIMITED = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_LIMITED_SPEED_ACK)
    ENGINEER_SPEED_NORMAL = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_NORMAL_SPEED_ACK)
    ENGINEER_SPEED_HIGHBALL = TMCC2ParameterCommandDef(TMCC2_DIALOG_CONTROL_ENGINEER_HIGHBALL_SPEED_ACK)


"""
    Word #2 - RailSounds Effects trigger controls (index 0x4)
"""
TMCC2_RS_EFFECTS_PRIME_MOVER_OFF: int = 0x10
TMCC2_RS_EFFECTS_PRIME_MOVER_ON: int = 0x11
TMCC2_RS_EFFECTS_MASTER_VOLUME_DOWN: int = 0x12
TMCC2_RS_EFFECTS_MASTER_VOLUME_UP: int = 0x13
TMCC2_RS_EFFECTS_BLEND_VOLUME_DOWN: int = 0x14
TMCC2_RS_EFFECTS_BLEND_VOLUME_UP: int = 0x15
TMCC2_RS_EFFECTS_CYLINDER_CLEARING_ON: int = 0x20
TMCC2_RS_EFFECTS_CYLINDER_CLEARING_OFF: int = 0x21
TMCC2_RS_EFFECTS_WHEEL_SLIP_TRIGGER: int = 0x22
TMCC2_RS_EFFECTS_STANDBY_WARNING_BELL: int = 0x23
TMCC2_RS_EFFECTS_STANDBY_MODE_DISABLE: int = 0x24
TMCC2_RS_EFFECTS_STANDBY_MODE_ENABLE: int = 0x25
TMCC2_RS_EFFECTS_FORCE_COUPLER_IMPACT_COMPRESS: int = 0x26
TMCC2_RS_EFFECTS_FORCE_COUPLER_IMPACT_STRETCH: int = 0x27
TMCC2_RS_EFFECTS_CIRCUIT_BREAKER_MAIN_LIGHTS: int = 0x28
TMCC2_RS_EFFECTS_CIRCUIT_BREAKER_CAB_LIGHTS: int = 0x29
TMCC2_RS_EFFECTS_CIRCUIT_BREAKER_WORK_LIGHTS: int = 0x2A
TMCC2_RS_EFFECTS_SEQUENCE_CONTROL_OFF: int = 0x2C
TMCC2_RS_EFFECTS_SEQUENCE_CONTROL_ON: int = 0x2D

TMCC2_RS_EFFECTS_RESET_ODOMETER: int = 0x30
TMCC2_RS_EFFECTS_INCREMENT_FUEL_LOAD: int = 0x31

TMCC2_RS_EFFECTS_SOUND_SYSTEM_OFF = TMCC2_SOUND_OFF_COMMAND
TMCC2_RS_EFFECTS_SOUND_SYSTEM_ON = TMCC2_SOUND_ON_COMMAND


@verify(UNIQUE)
class TMCC2RailSoundsEffectsControl(TMCC2ParameterEnum):
    ADD_FUEL = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_INCREMENT_FUEL_LOAD)
    BLEND_DOWN = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_BLEND_VOLUME_DOWN)
    BLEND_UP = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_BLEND_VOLUME_UP)
    CAB_BREAKER = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_CIRCUIT_BREAKER_CAB_LIGHTS)
    COUPLER_COMPRESS = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_FORCE_COUPLER_IMPACT_COMPRESS)
    COUPLER_STRETCH = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_FORCE_COUPLER_IMPACT_COMPRESS)
    CYLINDER_OFF = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_CYLINDER_CLEARING_OFF)
    CYLINDER_ON = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_CYLINDER_CLEARING_ON)
    MAIN_BREAKER = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_CIRCUIT_BREAKER_MAIN_LIGHTS)
    PRIME_OFF = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_PRIME_MOVER_OFF)
    PRIME_ON = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_PRIME_MOVER_ON)
    RESET_ODOMETER = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_RESET_ODOMETER)
    SEQUENCE_CONTROL_OFF = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_SEQUENCE_CONTROL_OFF)
    SEQUENCE_CONTROL_ON = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_SEQUENCE_CONTROL_ON)
    STANDBY_BELL = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_STANDBY_WARNING_BELL)
    STANDBY_DISABLE = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_STANDBY_MODE_DISABLE)
    STANDBY_ENABLE = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_STANDBY_MODE_ENABLE)
    VOLUME_DOWN_RS = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_MASTER_VOLUME_DOWN)
    VOLUME_UP_RS = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_MASTER_VOLUME_UP)
    WHEEL_SLIP = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_WHEEL_SLIP_TRIGGER)
    WORK_BREAKER = TMCC2ParameterCommandDef(TMCC2_RS_EFFECTS_CIRCUIT_BREAKER_WORK_LIGHTS)


"""
    Word #2 - Effects controls (index 0xC)
"""
TMCC2_EFFECTS_CONTROL_SMOKE_OFF: int = 0x00
TMCC2_EFFECTS_CONTROL_SMOKE_LOW: int = 0x01
TMCC2_EFFECTS_CONTROL_SMOKE_MEDIUM: int = 0x02
TMCC2_EFFECTS_CONTROL_SMOKE_HIGH: int = 0x03
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_FRONT_UP_CAB2: int = 0x10
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_FRONT_DOWN_CAB2: int = 0x11
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_REAR_UP_CAB2: int = 0x12
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_REAR_DOWN_CAB2: int = 0x13
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_FRONT_UP: int = 0x19
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_FRONT_DOWN: int = 0x18
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_REAR_UP: int = 0x1B
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_REAR_DOWN: int = 0x1A
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_BOTH_UP: int = 0x1F
TMCC2_EFFECTS_CONTROL_PANTOGRAPH_BOTH_DOWN: int = 0x1E
TMCC2_EFFECTS_CONTROL_SUBWAY_LEFT_DOOR_OPEN_CAB2: int = 0x20
TMCC2_EFFECTS_CONTROL_SUBWAY_LEFT_DOOR_CLOSE_CAB2: int = 0x21
TMCC2_EFFECTS_CONTROL_SUBWAY_RIGHT_DOOR_OPEN_CAB2: int = 0x22
TMCC2_EFFECTS_CONTROL_SUBWAY_RIGHT_DOOR_CLOSE_CAB2: int = 0x23
TMCC2_EFFECTS_CONTROL_SUBWAY_LEFT_DOOR_CLOSE: int = 0x28
TMCC2_EFFECTS_CONTROL_SUBWAY_LEFT_DOOR_OPEN: int = 0x29
TMCC2_EFFECTS_CONTROL_SUBWAY_RIGHT_DOOR_CLOSE: int = 0x2A
TMCC2_EFFECTS_CONTROL_SUBWAY_RIGHT_DOOR_OPEN: int = 0x2B
TMCC2_EFFECTS_CONTROL_SUBWAY_BOTH_DOOR_CLOSE: int = 0x2E
TMCC2_EFFECTS_CONTROL_SUBWAY_BOTH_DOOR_OPEN: int = 0x2F
TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_ONE_ON: int = 0x30
TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_ONE_OFF: int = 0x31
TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_TWO_ON: int = 0x32
TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_TWO_OFF: int = 0x33
TMCC2_EFFECTS_CONTROL_STOCK_CAR_LOAD: int = 0x34
TMCC2_EFFECTS_CONTROL_STOCK_CAR_UNLOAD: int = 0x35
TMCC2_EFFECTS_CONTROL_STOCK_CAR_FRED_ON: int = 0x36
TMCC2_EFFECTS_CONTROL_STOCK_CAR_FRED_OFF: int = 0x37
TMCC2_EFFECTS_CONTROL_STOCK_CAR_FLAT_WHEEL_ON: int = 0x38
TMCC2_EFFECTS_CONTROL_STOCK_CAR_FLAT_WHEEL_OFF: int = 0x39
TMCC2_EFFECTS_CONTROL_STOCK_CAR_GAME_ON: int = 0x3A
TMCC2_EFFECTS_CONTROL_STOCK_CAR_GAME_OFF: int = 0x3B
TMCC2_EFFECTS_CONTROL_SCENE_ZERO: int = 0x3C
TMCC2_EFFECTS_CONTROL_SCENE_ONE: int = 0x3D
TMCC2_EFFECTS_CONTROL_SCENE_TWO: int = 0x3E
TMCC2_EFFECTS_CONTROL_SCENE_THREE: int = 0x3F
TMCC2_EFFECTS_CONTROL_COAL_EMPTY: int = 0x50
TMCC2_EFFECTS_CONTROL_COAL_FULL: int = 0x51
TMCC2_EFFECTS_CONTROL_COAL_EMPTYING: int = 0x52
TMCC2_EFFECTS_CONTROL_COAL_FILLING: int = 0x53


@verify(UNIQUE)
class TMCC2EffectsControl(TMCC2ParameterEnum):
    PANTO_FRONT_DOWN = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_PANTOGRAPH_FRONT_DOWN)
    PANTO_FRONT_UP = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_PANTOGRAPH_FRONT_UP)
    PANTO_REAR_DOWN = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_PANTOGRAPH_REAR_DOWN)
    PANTO_REAR_UP = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_PANTOGRAPH_REAR_UP)
    PANTO_BOTH_DOWN = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_PANTOGRAPH_BOTH_DOWN)
    PANTO_BOTH_UP = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_PANTOGRAPH_BOTH_UP)
    SMOKE_HIGH = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SMOKE_HIGH)
    SMOKE_LOW = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SMOKE_LOW)
    SMOKE_MEDIUM = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SMOKE_MEDIUM)
    SMOKE_OFF = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SMOKE_OFF)
    STOCK_FRED_OFF = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_FRED_OFF)
    STOCK_FRED_ON = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_FRED_ON)
    STOCK_GAME_OFF = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_GAME_OFF)
    STOCK_GAME_ON = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_GAME_ON)
    STOCK_LOAD = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_LOAD)
    STOCK_OPTION_ONE_OFF = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_ONE_OFF)
    STOCK_OPTION_ONE_ON = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_ONE_ON)
    STOCK_OPTION_ONE_TWO = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_TWO_OFF)
    STOCK_OPTION_TWO_ON = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_OPTION_TWO_ON)
    STOCK_UNLOAD = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_UNLOAD)
    STOCK_WHEEL_OFF = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_FLAT_WHEEL_OFF)
    STOCK_WHEEL_ON = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_STOCK_CAR_FLAT_WHEEL_ON)
    SUBWAY_LEFT_DOOR_CLOSE = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SUBWAY_LEFT_DOOR_CLOSE)
    SUBWAY_LEFT_DOOR_OPEN = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SUBWAY_LEFT_DOOR_OPEN)
    SUBWAY_RIGHT_DOOR_CLOSE = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SUBWAY_RIGHT_DOOR_CLOSE)
    SUBWAY_RIGHT_DOOR_OPEN = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SUBWAY_RIGHT_DOOR_OPEN)
    SUBWAY_BOTH_DOOR_CLOSE = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SUBWAY_BOTH_DOOR_CLOSE)
    SUBWAY_BOTH_DOOR_OPEN = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_SUBWAY_BOTH_DOOR_OPEN)
    COAL_EMPTY = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_COAL_EMPTY)
    COAL_FULL = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_COAL_FULL)
    COAL_EMPTYING = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_COAL_EMPTYING)
    COAL_FILLING = TMCC2ParameterCommandDef(TMCC2_EFFECTS_CONTROL_COAL_FILLING)


"""
    Word #2 - Lighting controls (index 0xD)
"""
TMCC2_LIGHTING_CONTROL_CAB_LIGHT_AUTO: int = 0xF2
TMCC2_LIGHTING_CONTROL_CAB_LIGHT_OFF: int = 0xF0
TMCC2_LIGHTING_CONTROL_CAB_LIGHT_ON: int = 0xF1
TMCC2_LIGHTING_CONTROL_CAR_LIGHT_AUTO: int = 0xFA
TMCC2_LIGHTING_CONTROL_CAR_LIGHT_OFF: int = 0xF8
TMCC2_LIGHTING_CONTROL_CAR_LIGHT_ON: int = 0xF9
TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_OFF: int = 0xC0
TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_OFF_PULSE_ON_WITH_HORN: int = 0xC1
TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_ON: int = 0xC3
TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_ON_PULSE_OFF_WITH_HORN: int = 0xC2
TMCC2_LIGHTING_CONTROL_DOGHOUSE_LIGHT_OFF: int = 0xA0
TMCC2_LIGHTING_CONTROL_DOGHOUSE_LIGHT_ON: int = 0xA1
TMCC2_LIGHTING_CONTROL_GROUND_LIGHT_AUTO: int = 0xD2
TMCC2_LIGHTING_CONTROL_GROUND_LIGHT_OFF: int = 0xD0
TMCC2_LIGHTING_CONTROL_GROUND_LIGHT_ON: int = 0xD1
TMCC2_LIGHTING_CONTROL_HAZARD_LIGHT_OFF: int = 0xB0
TMCC2_LIGHTING_CONTROL_HAZARD_LIGHT_ON: int = 0xB1
TMCC2_LIGHTING_CONTROL_HAZARD_LIGHT_AUTO: int = 0xB2
TMCC2_LIGHTING_CONTROL_LOCO_MARKER_LIGHT_OFF: int = 0xC8
TMCC2_LIGHTING_CONTROL_LOCO_MARKER_LIGHT_ON: int = 0xC9
TMCC2_LIGHTING_CONTROL_LOCO_MARKER_LIGHT_AUTO: int = 0xCA
TMCC2_LIGHTING_CONTROL_MARS_LIGHT_OFF: int = 0xE8
TMCC2_LIGHTING_CONTROL_MARS_LIGHT_ON: int = 0xE9
TMCC2_LIGHTING_CONTROL_RULE_17_AUTO: int = 0xF6
TMCC2_LIGHTING_CONTROL_RULE_17_OFF: int = 0xF4
TMCC2_LIGHTING_CONTROL_RULE_17_ON: int = 0xF5
TMCC2_LIGHTING_CONTROL_STROBE_LIGHT_OFF: int = 0xE0
TMCC2_LIGHTING_CONTROL_STROBE_LIGHT_ON_DOUBLE_FLASH: int = 0xE2
TMCC2_LIGHTING_CONTROL_STROBE_LIGHT_ON_SINGLE_FLASH: int = 0xE1
TMCC2_LIGHTING_CONTROL_TENDER_MARKER_LIGHT_OFF: int = 0xCC
TMCC2_LIGHTING_CONTROL_TENDER_MARKER_LIGHT_ON: int = 0xCD
TMCC2_LIGHTING_CONTROL_WORK_LIGHT_OFF: int = 0xD8
TMCC2_LIGHTING_CONTROL_WORK_LIGHT_ON: int = 0xD9
TMCC2_LIGHTING_CONTROL_WORK_LIGHT_AUTO: int = 0xDA


@verify(UNIQUE)
class TMCC2LightingControl(TMCC2ParameterEnum):
    CAB_AUTO = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_CAB_LIGHT_AUTO)
    CAB_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_CAB_LIGHT_OFF)
    CAB_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_CAB_LIGHT_ON)
    CAR_AUTO = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_CAR_LIGHT_AUTO)
    CAR_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_CAR_LIGHT_OFF)
    CAR_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_CAR_LIGHT_ON)
    DITCH_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_OFF)
    DITCH_OFF_PULSE_ON_WITH_HORN = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_OFF_PULSE_ON_WITH_HORN)
    DITCH_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_ON)
    DITCH_ON_PULSE_OFF_WITH_HORN = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_DITCH_LIGHT_ON_PULSE_OFF_WITH_HORN)
    DOGHOUSE_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_DOGHOUSE_LIGHT_OFF)
    DOGHOUSE_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_DOGHOUSE_LIGHT_ON)
    GROUND_AUTO = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_GROUND_LIGHT_AUTO)
    GROUND_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_GROUND_LIGHT_OFF)
    GROUND_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_GROUND_LIGHT_ON)
    HAZARD_AUTO = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_HAZARD_LIGHT_AUTO)
    HAZARD_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_HAZARD_LIGHT_OFF)
    HAZARD_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_HAZARD_LIGHT_ON)
    LOCO_MARKER_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_LOCO_MARKER_LIGHT_OFF)
    LOCO_MARKER_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_LOCO_MARKER_LIGHT_ON)
    LOCO_MARKER_AUTO = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_LOCO_MARKER_LIGHT_AUTO)
    MARS_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_MARS_LIGHT_OFF)
    MARS_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_MARS_LIGHT_ON)
    RULE_17_AUTO = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_RULE_17_AUTO)
    RULE_17_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_RULE_17_OFF)
    RULE_17_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_RULE_17_ON)
    STROBE_LIGHT_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_STROBE_LIGHT_OFF)
    STROBE_LIGHT_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_STROBE_LIGHT_ON_SINGLE_FLASH)
    STROBE_LIGHT_ON_DOUBLE = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_STROBE_LIGHT_ON_DOUBLE_FLASH)
    TENDER_MARKER_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_TENDER_MARKER_LIGHT_OFF)
    TENDER_MARKER_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_TENDER_MARKER_LIGHT_ON)
    WORK_AUTO = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_WORK_LIGHT_AUTO)
    WORK_OFF = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_WORK_LIGHT_OFF)
    WORK_ON = TMCC2ParameterCommandDef(TMCC2_LIGHTING_CONTROL_WORK_LIGHT_ON)
