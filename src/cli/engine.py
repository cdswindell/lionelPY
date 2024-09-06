#!/usr/bin/env python3
#
import argparse

from src.cli.cli_base import CliBaseTMCC, DataAction, cli_parser, command_format_parser, train_parser
from src.protocol.constants import EngineOptionEnum, TMCC1EngineOption, TMCC2EngineOption
from src.protocol.tmcc1.engine_cmd import EngineCmd as EngineCmdTMCC1
from src.protocol.tmcc2.engine_cmd import EngineCmd as EngineCmdTMCC2


class EngineCli(CliBaseTMCC):
    def __init__(self, arg_parser: argparse.ArgumentParser) -> None:
        super().__init__(arg_parser)
        engine: int = self._args.engine
        option_data: int = self._args.data if 'data' in self._args else 0
        try:
            option: EngineOptionEnum = self._decode_option()  # raise ValueError if can't decode
            scope = self._determine_scope()
            if self.is_tmcc2 or isinstance(option, TMCC2EngineOption):
                cmd = EngineCmdTMCC2(engine,
                                     TMCC2EngineOption(option),
                                     option_data,
                                     scope,
                                     baudrate=self._args.baudrate,
                                     port=self._args.port)
            else:
                cmd = EngineCmdTMCC1(engine,
                                     TMCC1EngineOption(option),
                                     option_data,
                                     scope,
                                     baudrate=self._args.baudrate,
                                     port=self._args.port)
            cmd.fire()
        except ValueError as ve:
            print(ve)


if __name__ == '__main__':
    engine_parser = argparse.ArgumentParser(add_help=False)
    engine_parser.add_argument("engine", metavar='Engine/Train', type=int, help="Engine/Train to control")

    ops = engine_parser.add_mutually_exclusive_group()
    ops.add_argument("-a", "--set_address",
                     action="store_const",
                     const='SET_ADDRESS',
                     dest='option',
                     help="Set engine address")

    ops.add_argument("-s", "--stop_immediate",
                     action="store_const",
                     const='STOP_IMMEDIATE',
                     dest='option',
                     help="Stop immediate")

    ops.add_argument("-fwd", "--forward_direction",
                     action="store_const",
                     const='FORWARD_DIRECTION',
                     dest='option',
                     help="Set forward direction")

    ops.add_argument("-rev", "--reverse_direction",
                     action="store_const",
                     const='REVERSE_DIRECTION',
                     dest='option',
                     help="Set reverse direction")

    ops.add_argument("-t", "--toggle_direction",
                     action="store_const",
                     const='TOGGLE_DIRECTION',
                     dest='option',
                     help="Toggle direction")

    ops.add_argument("-fc", "--front_coupler",
                     action="store_const",
                     const='FRONT_COUPLER',
                     dest='option',
                     help="Open front coupler")

    ops.add_argument("-rc", "--rear_coupler",
                     action="store_const",
                     const='REAR_COUPLER',
                     dest='option',
                     help="Open rear coupler")

    ops.add_argument("-r", "--ring_bell",
                     action="store_const",
                     const='RING_BELL',
                     dest='option',
                     help="Ring bell")

    ops.add_argument("-b", "--blow_horn",
                     action="store_const",
                     const='BLOW_HORN_ONE',
                     dest='option',
                     help="Blow horn")

    ops.add_argument("-boost", "--boost_speed",
                     action="store_const",
                     const='BOOST_SPEED',
                     dest='option',
                     help="Brake speed")

    ops.add_argument("-bl", "--boost_level",
                     action=DataAction,
                     dest='option',
                     choices=range(0, 8),
                     metavar="0 - 7",
                     type=int,
                     nargs='?',
                     default=3,
                     const='BOOST_LEVEL',
                     help="Boost level")

    ops.add_argument("-brake", "--brake_speed",
                     action="store_const",
                     const='BRAKE_SPEED',
                     dest='option',
                     help="Boost speed")

    ops.add_argument("-kl", "--brake_level",
                     action=DataAction,
                     dest='option',
                     choices=range(0, 8),
                     metavar="0 - 7",
                     type=int,
                     nargs='?',
                     default=3,
                     const='BRAKE_LEVEL',
                     help="Brake level")

    ops.add_argument("-sui", "--start_up_immediate",
                     action="store_const",
                     const='START_UP_IMMEDIATE',
                     dest='option',
                     help="Start up immediate")

    ops.add_argument("-sud", "--start_up_delayed",
                     action="store_const",
                     const='START_UP_DELAYED',
                     dest='option',
                     help="Start up delayed (prime mover)")

    ops.add_argument("-sdi", "--shutdown_immediate",
                     action="store_const",
                     const='SHUTDOWN_IMMEDIATE',
                     dest='option',
                     help="Shutdown Immediate")

    ops.add_argument("-sdd", "--shutdown_delayed",
                     action="store_const",
                     const='SHUTDOWN_DELAYED',
                     dest='option',
                     help="Shutdown delayed with announcement")

    # create subparsers to handle train/engine-specific operations
    sp = engine_parser.add_subparsers(dest='command', help='Engine/train sub-commands')

    # Speed operations
    speed = sp.add_parser('speed', aliases=['sp'], help='Speed of engine/train')
    speed.add_argument('data',
                       type=int,
                       action='store',
                       help="Absolute/Relative speed")
    speed_group = speed.add_mutually_exclusive_group()
    speed_group.add_argument("-a", "--absolute",
                             action="store_const",
                             const='ABSOLUTE_SPEED',
                             dest='option',
                             help="Set absolute speed")
    speed_group.add_argument("-r", "--relative",
                             action="store_const",
                             const='RELATIVE_SPEED',
                             dest='option',
                             help="Set relative speed speed (-5 to 5)")
    speed_group.set_defaults(option='ABSOLUTE_SPEED')

    # Bell operations
    bell = sp.add_parser('bell', aliases=['be'], help='Bell operations')
    bell_group = bell.add_mutually_exclusive_group()
    bell_group.add_argument("-r", "--ring",
                            action="store_const",
                            const='RING_BELL',
                            dest='option',
                            default='RING_BELL',
                            help="Ring bell")
    bell_group.add_argument("-on",
                            action="store_const",
                            const='BELL_ON',
                            dest='option',
                            help="Turn bell on")
    bell_group.add_argument("-off",
                            action="store_const",
                            const='BELL_OFF',
                            dest='option',
                            help="Turn bell off")
    bell_group.add_argument("-d", "--ding",
                            action=DataAction,
                            dest='option',
                            choices=range(0, 4),
                            metavar="0 - 3",
                            type=int,
                            nargs='?',
                            default=3,
                            const='BELL_ONE_SHOT_DING',
                            help="Bell one shot ding")
    bell_group.add_argument("-s", "--slider",
                            action=DataAction,
                            dest='option',
                            choices=range(2, 6),
                            metavar="2 - 5",
                            type=int,
                            nargs='?',
                            default=2,
                            const='BELL_SLIDER_POSITION',
                            help="Bell slider position")

    # Horn operations
    horn = sp.add_parser('horn', aliases=['ho'], help='Horn operations')
    horn_group = horn.add_mutually_exclusive_group()
    horn_group.add_argument("-1", "--blow_horn_one",
                            action="store_const",
                            const='BLOW_HORN_ONE',
                            dest='option',
                            default='BLOW_HORN_ONE',
                            help="Blow horn One")
    horn_group.add_argument("-2", "--blow_horn_two",
                            action="store_const",
                            const='BLOW_HORN_TWO',
                            dest='option',
                            help="Blow horn two")
    horn_group.add_argument("-i", "--intensity",
                            action=DataAction,
                            dest='option',
                            choices=range(0, 17),
                            metavar="0 - 16",
                            type=int,
                            nargs='?',
                            default=1,
                            const='QUILLING_HORN_INTENSITY',
                            help="Quilling horn intensity")

    # Momentum operations
    momentum = sp.add_parser('momentum', aliases=['mo'], help='Momentum operations')
    mom_group = momentum.add_mutually_exclusive_group()
    mom_group.add_argument("-l", "--low",
                           action="store_const",
                           const='MOMENTUM_LOW',
                           dest='option',
                           default='MOMENTUM_MEDIUM',  # strange, but default actions only applied if placed
                           help="Set momentum to low")  # on first argument of mutual group
    mom_group.add_argument("-m", "--medium",
                           action="store_const",
                           const='MOMENTUM_MEDIUM',
                           dest='option',
                           help="Set momentum to medium")
    mom_group.add_argument("-x", "--high",
                           action="store_const",
                           const='MOMENTUM_HIGH',
                           dest='option',
                           help="Set momentum to high")
    mom_group.add_argument("-off",
                           action="store_const",
                           const='MOMENTUM',
                           dest='option',
                           help="Set momentum off")

    mom_group.add_argument("-a", "--absolute",
                           action=DataAction,
                           dest='option',
                           choices=range(0, 8),
                           metavar="0 - 7",
                           type=int,
                           nargs='?',
                           default=0,
                           const='MOMENTUM',
                           help="Set absolute momentum")

    sound = sp.add_parser('sound', aliases=['so'], help='Sound operations')
    sound_group = sound.add_mutually_exclusive_group(required=True)
    sound_group.add_argument("-d", "--diesel_run_level",
                             action=DataAction,
                             dest='option',
                             choices=range(0, 8),
                             metavar="0 - 7",
                             type=int,
                             nargs='?',
                             default=0,
                             const='DIESEL_LEVEL',
                             help="Diesel run level")
    sound_group.add_argument("-e", "--engine_labor",
                             action=DataAction,
                             dest='option',
                             choices=range(0, 32),
                             metavar="0 - 31",
                             type=int,
                             nargs='?',
                             default=0,
                             const='ENGINE_LABOR',
                             help="Engine labor")
    sound_group.add_argument("-l", "--let_off",
                             action="store_const",
                             const='LET_OFF',
                             dest='option',
                             help="Let off sound")

    # construct final parser with all components in order
    parser = argparse.ArgumentParser("Control specified engine/train (1 - 99)",
                                     parents=[engine_parser,
                                              train_parser(),
                                              command_format_parser(),
                                              cli_parser()])
    EngineCli(parser)
