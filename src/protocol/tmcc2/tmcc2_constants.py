import abc
from enum import verify, UNIQUE
from typing import Dict

from src.protocol.command_def import CommandDef, CommandDefEnum
from src.protocol.constants import CommandPrefix, CommandScope, RELATIVE_SPEED_MAP, CommandSyntax

LEGACY_EXTENDED_BLOCK_COMMAND_PREFIX: int = 0xFA
LEGACY_PARAMETER_COMMAND_PREFIX: int = 0xFB
LEGACY_ENGINE_COMMAND_PREFIX: int = 0xF8
LEGACY_TRAIN_COMMAND_PREFIX: int = 0xF9

"""
    TMCC2 constants
"""


class TMCC2Enum(CommandDefEnum):
    """
        Marker Interface for all TMCC2 enums
    """
    pass


"""
    Legacy/TMCC2 Protocol/first_byte Constants
"""


# All Legacy/TMCC2 commands begin with one of the following 1 byte sequences
# Engine/Train/Parameter 2 digit address are first 7 bits of first byte


@verify(UNIQUE)
class TMCC2CommandPrefix(CommandPrefix):
    ENGINE = LEGACY_ENGINE_COMMAND_PREFIX
    TRAIN = LEGACY_TRAIN_COMMAND_PREFIX
    ROUTE = LEGACY_EXTENDED_BLOCK_COMMAND_PREFIX  # probably used for other things
    PARAMETER = LEGACY_PARAMETER_COMMAND_PREFIX


TMCC2_FIRST_BYTE_TO_SCOPE_MAP = {
    TMCC2CommandPrefix.ENGINE: CommandScope.ENGINE,
    TMCC2CommandPrefix.TRAIN: CommandScope.TRAIN,
    TMCC2CommandPrefix.ROUTE: CommandScope.ROUTE,
}

TMCC2_SCOPE_TO_FIRST_BYTE_MAP = {s: p for p, s in TMCC2_FIRST_BYTE_TO_SCOPE_MAP.items()}


class TMCC2CommandDef(CommandDef):
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 command_bits: int,
                 scope: CommandScope = CommandScope.ENGINE,
                 is_addressable: bool = True,
                 d_min: int = 0,
                 d_max: int = 0,
                 d_map: Dict[int, int] = None) -> None:
        super().__init__(command_bits, is_addressable, d_min=d_min, d_max=d_max, d_map=d_map)
        self._scope = scope

    @property
    def first_byte(self) -> bytes:
        return TMCC2_SCOPE_TO_FIRST_BYTE_MAP[self.scope].to_bytes(1, byteorder='big')

    @property
    def scope(self) -> CommandScope:
        return self._scope

    @property
    def syntax(self) -> CommandSyntax:
        return CommandSyntax.TMCC2

    @property
    def address_mask(self) -> int:
        return 0xFFFF & ~((2 ** self.num_address_bits - 1) << 9)


TMCC2_HALT_COMMAND: int = 0x01AB


@verify(UNIQUE)
class TMCC2HaltCommandDef(TMCC2Enum):
    HALT = TMCC2CommandDef(TMCC2_HALT_COMMAND, CommandScope.ENGINE)


# The TMCC2 route command is an undocumented "extended block command" (0xFA)
LEGACY_ROUTE_COMMAND: int = 0x00FD


@verify(UNIQUE)
class TMCC2RouteCommandDef(TMCC2Enum):
    ROUTE = TMCC2CommandDef(LEGACY_ROUTE_COMMAND, scope=CommandScope.ROUTE)


TMCC2_SET_ABSOLUTE_SPEED_COMMAND: int = 0x0000  # encode speed in last byte (0 - 199)
TMCC2_SET_MOMENTUM_COMMAND: int = 0x00C8  # encode momentum in last 3 bits (0 - 7)
TMCC2_SET_BRAKE_LEVEL_COMMAND: int = 0x00E0  # encode brake level in last 3 bits (0 - 7)
TMCC2_SET_BOOST_LEVEL_COMMAND: int = 0x00E8  # encode boost level in last 3 bits (0 - 7)
TMCC2_SET_TRAIN_BRAKE_COMMAND: int = 0x00F0  # encode train brake in last 3 bits (0 - 7)
TMCC2_STALL_COMMAND: int = 0x00F8
TMCC2_STOP_IMMEDIATE_COMMAND: int = 0x00FB
TMCC2_FORWARD_DIRECTION_COMMAND: int = 0x0100
TMCC2_TOGGLE_DIRECTION_COMMAND: int = 0x0101
TMCC2_REVERSE_DIRECTION_COMMAND: int = 0x0103
TMCC2_OPEN_FRONT_COUPLER_COMMAND: int = 0x0105
TMCC2_OPEN_REAR_COUPLER_COMMAND: int = 0x0106
TMCC2_RING_BELL_COMMAND: int = 0x011D
TMCC2_BELL_OFF_COMMAND: int = 0x01F4
TMCC2_BELL_ON_COMMAND: int = 0x01F5
TMCC2_BELL_ONE_SHOT_DING_COMMAND: int = 0x01F0  # encode ding in last 2 bits (0 - 3)
TMCC2_BELL_SLIDER_POSITION_COMMAND: int = 0x01B0  # encode position in last 3 bits (2 - 5)
TMCC2_BLOW_HORN_ONE_COMMAND: int = 0x011C
TMCC2_BLOW_HORN_TWO_COMMAND: int = 0x011F
TMCC2_QUILLING_HORN_INTENSITY_COMMAND: int = 0x01E0
TMCC2_SET_MOMENTUM_LOW_COMMAND: int = 0x0128
TMCC2_SET_MOMENTUM_MEDIUM_COMMAND: int = 0x0129
TMCC2_SET_MOMENTUM_HIGH_COMMAND: int = 0x012A
TMCC2_BOOST_SPEED_COMMAND: int = 0x0104
TMCC2_BRAKE_SPEED_COMMAND: int = 0x0107
TMCC2_NUMERIC_COMMAND: int = 0x0110
TMCC2_ENG_LET_OFF_SOUND_COMMAND: int = 0x01F9
TMCC2_ENG_LET_OFF_LONG_SOUND_COMMAND: int = 0x01FA
TMCC2_WATER_INJECTOR_SOUND_COMMAND: int = 0x01A8
TMCC2_ENG_BRAKE_SQUEAL_SOUND_COMMAND: int = 0x01F6
TMCC2_ENG_AUGER_SOUND_COMMAND: int = 0x01F7
TMCC2_ENG_BRAKE_AIR_RELEASE_SOUND_COMMAND: int = 0x01F8
TMCC2_ENG_REFUELLING_SOUND_COMMAND: int = 0x012D
TMCC2_DIESEL_RUN_LEVEL_SOUND_COMMAND: int = 0x01A0  # run level 0 - 7 encoded in last 3 bits
TMCC2_ENGINE_LABOR_COMMAND: int = 0x01C0  # engine labor 0 - 31 encoded in last 5 bytes
TMCC2_START_UP_SEQ_ONE_COMMAND: int = 0x01FB
TMCC2_START_UP_SEQ_TWO_COMMAND: int = 0x01FC
TMCC2_SHUTDOWN_SEQ_ONE_COMMAND: int = 0x01FD
TMCC2_SHUTDOWN_SEQ_TWO_COMMAND: int = 0x01FE
TMCC2_AUX1_OFF_COMMAND: int = 0x0108
TMCC2_AUX1_OPTION_ONE_COMMAND: int = 0x0109  # Cab 1 Aux1 button
TMCC2_AUX1_OPTION_TWO_COMMAND: int = 0x010A
TMCC2_AUX1_ON_COMMAND: int = 0x010B
TMCC2_AUX2_OFF_COMMAND: int = 0x010C
TMCC2_AUX2_OPTION_ONE_COMMAND: int = 0x010D  # Cab 1 Aux2 button
TMCC2_AUX2_OPTION_TWO_COMMAND: int = 0x010E
TMCC2_AUX2_ON_COMMAND: int = 0x010F
TMCC2_SET_ADDRESS_COMMAND: int = 0x012B
TMCC2_SET_RELATIVE_SPEED_COMMAND: int = 0x0140  # Relative Speed -5 - 5 encoded in last 4 bits (offset by 5)
TMCC2_ROLL_SPEED: int = 1  # express speeds as simple integers
TMCC2_RESTRICTED_SPEED: int = 24
TMCC2_SLOW_SPEED: int = 59
TMCC2_MEDIUM_SPEED: int = 92
TMCC2_LIMITED_SPEED: int = 118
TMCC2_NORMAL_SPEED: int = 145
TMCC2_HIGHBALL_SPEED: int = 199

TMCC2_SPEED_MAP = dict(ROLL=TMCC2_ROLL_SPEED, RO=TMCC2_ROLL_SPEED,
                       RESTRICTED=TMCC2_RESTRICTED_SPEED, RE=TMCC2_RESTRICTED_SPEED,
                       SLOW=TMCC2_SLOW_SPEED, SL=TMCC2_SLOW_SPEED,
                       MEDIUM=TMCC2_MEDIUM_SPEED, ME=TMCC2_MEDIUM_SPEED,
                       LIMITED=TMCC2_LIMITED_SPEED, LI=TMCC2_LIMITED_SPEED,
                       NORMAL=TMCC2_NORMAL_SPEED, NO=TMCC2_NORMAL_SPEED,
                       HIGH=TMCC2_HIGHBALL_SPEED, HIGHBALL=TMCC2_HIGHBALL_SPEED, HI=TMCC2_HIGHBALL_SPEED)


@verify(UNIQUE)
class TMCC2EngineCommandDef(TMCC2Enum):
    ABSOLUTE_SPEED = TMCC2CommandDef(TMCC2_SET_ABSOLUTE_SPEED_COMMAND, d_max=199)
    AUGER = TMCC2CommandDef(TMCC2_ENG_AUGER_SOUND_COMMAND)
    AUX1_OFF = TMCC2CommandDef(TMCC2_AUX1_OFF_COMMAND)
    AUX1_ON = TMCC2CommandDef(TMCC2_AUX1_ON_COMMAND)
    AUX1_OPTION_ONE = TMCC2CommandDef(TMCC2_AUX1_OPTION_ONE_COMMAND)
    AUX1_OPTION_TWO = TMCC2CommandDef(TMCC2_AUX1_OPTION_TWO_COMMAND)
    AUX2_OFF = TMCC2CommandDef(TMCC2_AUX2_OFF_COMMAND)
    AUX2_ON = TMCC2CommandDef(TMCC2_AUX2_ON_COMMAND)
    AUX2_OPTION_ONE = TMCC2CommandDef(TMCC2_AUX2_OPTION_ONE_COMMAND)
    AUX2_OPTION_TWO = TMCC2CommandDef(TMCC2_AUX2_OPTION_TWO_COMMAND)
    BELL_OFF = TMCC2CommandDef(TMCC2_BELL_OFF_COMMAND)
    BELL_ON = TMCC2CommandDef(TMCC2_BELL_ON_COMMAND)
    BELL_ONE_SHOT_DING = TMCC2CommandDef(TMCC2_BELL_ONE_SHOT_DING_COMMAND, d_max=3)
    BELL_SLIDER_POSITION = TMCC2CommandDef(TMCC2_BELL_SLIDER_POSITION_COMMAND, d_min=2, d_max=5)
    BLOW_HORN_ONE = TMCC2CommandDef(TMCC2_BLOW_HORN_ONE_COMMAND)
    BLOW_HORN_TWO = TMCC2CommandDef(TMCC2_BLOW_HORN_TWO_COMMAND)
    BOOST_LEVEL = TMCC2CommandDef(TMCC2_SET_BOOST_LEVEL_COMMAND, d_max=7)
    BOOST_SPEED = TMCC2CommandDef(TMCC2_BOOST_SPEED_COMMAND)
    BRAKE_AIR_RELEASE = TMCC2CommandDef(TMCC2_ENG_BRAKE_AIR_RELEASE_SOUND_COMMAND)
    BRAKE_LEVEL = TMCC2CommandDef(TMCC2_SET_BRAKE_LEVEL_COMMAND, d_max=7)
    BRAKE_SPEED = TMCC2CommandDef(TMCC2_BRAKE_SPEED_COMMAND)
    BRAKE_SQUEAL = TMCC2CommandDef(TMCC2_ENG_BRAKE_SQUEAL_SOUND_COMMAND)
    DIESEL_LEVEL = TMCC2CommandDef(TMCC2_DIESEL_RUN_LEVEL_SOUND_COMMAND, d_max=7)
    ENGINE_LABOR = TMCC2CommandDef(TMCC2_ENGINE_LABOR_COMMAND, d_max=31)
    FORWARD_DIRECTION = TMCC2CommandDef(TMCC2_FORWARD_DIRECTION_COMMAND)
    FRONT_COUPLER = TMCC2CommandDef(TMCC2_OPEN_FRONT_COUPLER_COMMAND)
    LET_OFF = TMCC2CommandDef(TMCC2_ENG_LET_OFF_SOUND_COMMAND)
    LET_OFF_LONG = TMCC2CommandDef(TMCC2_ENG_LET_OFF_LONG_SOUND_COMMAND)
    MOMENTUM = TMCC2CommandDef(TMCC2_SET_MOMENTUM_COMMAND, d_max=7)
    MOMENTUM_HIGH = TMCC2CommandDef(TMCC2_SET_MOMENTUM_HIGH_COMMAND)
    MOMENTUM_LOW = TMCC2CommandDef(TMCC2_SET_MOMENTUM_LOW_COMMAND)
    MOMENTUM_MEDIUM = TMCC2CommandDef(TMCC2_SET_MOMENTUM_MEDIUM_COMMAND)
    NUMERIC = TMCC2CommandDef(TMCC2_NUMERIC_COMMAND, d_max=9)
    QUILLING_HORN_INTENSITY = TMCC2CommandDef(TMCC2_QUILLING_HORN_INTENSITY_COMMAND, d_max=15)
    REAR_COUPLER = TMCC2CommandDef(TMCC2_OPEN_REAR_COUPLER_COMMAND)
    REFUELLING = TMCC2CommandDef(TMCC2_ENG_REFUELLING_SOUND_COMMAND)
    RELATIVE_SPEED = TMCC2CommandDef(TMCC2_SET_RELATIVE_SPEED_COMMAND, d_map=RELATIVE_SPEED_MAP)
    REVERSE_DIRECTION = TMCC2CommandDef(TMCC2_REVERSE_DIRECTION_COMMAND)
    RING_BELL = TMCC2CommandDef(TMCC2_RING_BELL_COMMAND)
    SET_ADDRESS = TMCC2CommandDef(TMCC2_SET_ADDRESS_COMMAND)
    SHUTDOWN_DELAYED = TMCC2CommandDef(TMCC2_SHUTDOWN_SEQ_ONE_COMMAND)
    SHUTDOWN_IMMEDIATE = TMCC2CommandDef(TMCC2_SHUTDOWN_SEQ_TWO_COMMAND)
    SPEED_HIGH_BALL = TMCC2CommandDef(TMCC2_SET_ABSOLUTE_SPEED_COMMAND | TMCC2_HIGHBALL_SPEED)
    SPEED_LIMITED = TMCC2CommandDef(TMCC2_SET_ABSOLUTE_SPEED_COMMAND | TMCC2_LIMITED_SPEED)
    SPEED_MEDIUM = TMCC2CommandDef(TMCC2_SET_ABSOLUTE_SPEED_COMMAND | TMCC2_MEDIUM_SPEED)
    SPEED_NORMAL = TMCC2CommandDef(TMCC2_SET_ABSOLUTE_SPEED_COMMAND | TMCC2_NORMAL_SPEED)
    SPEED_RESTRICTED = TMCC2CommandDef(TMCC2_SET_ABSOLUTE_SPEED_COMMAND | TMCC2_RESTRICTED_SPEED)
    SPEED_ROLL = TMCC2CommandDef(TMCC2_ROLL_SPEED | TMCC2_ROLL_SPEED)
    SPEED_SLOW = TMCC2CommandDef(TMCC2_SET_ABSOLUTE_SPEED_COMMAND | TMCC2_SLOW_SPEED)
    STALL = TMCC2CommandDef(TMCC2_STALL_COMMAND)
    START_UP_DELAYED = TMCC2CommandDef(TMCC2_START_UP_SEQ_ONE_COMMAND)
    START_UP_IMMEDIATE = TMCC2CommandDef(TMCC2_START_UP_SEQ_TWO_COMMAND)
    STOP_IMMEDIATE = TMCC2CommandDef(TMCC2_STOP_IMMEDIATE_COMMAND)
    SYSTEM_HALT = TMCC2CommandDef(TMCC2_HALT_COMMAND)
    TOGGLE_DIRECTION = TMCC2CommandDef(TMCC2_TOGGLE_DIRECTION_COMMAND)
    TRAIN_BRAKE = TMCC2CommandDef(TMCC2_SET_TRAIN_BRAKE_COMMAND, d_max=7)
    WATER_INJECTOR = TMCC2CommandDef(TMCC2_WATER_INJECTOR_SOUND_COMMAND)
