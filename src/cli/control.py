#!/usr/bin/env python3
#
import argparse
import readline

from src.cli.cli_base import cli_parser
from src.cli.acc import AccCli
from src.cli.engine import EngineCli
from src.cli.halt import HaltCli
from src.cli.lighting import LightingCli
from src.cli.route import RouteCli
from src.cli.switch import SwitchCli
from src.comm.comm_buffer import CommBuffer, CommBufferSingleton
from src.comm.enqueue_proxy_requests import EnqueueProxyRequests
from src.protocol.constants import DEFAULT_SERVER_PORT
from src.utils.argument_parser import ArgumentParser


class TrainControl:
    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args
        self._baudrate = args.baudrate
        self._server, self._port = CommBuffer.parse_server(args.server, args.port, args.server_port)
        self._comm_buffer = CommBuffer.build(baudrate=self._baudrate,
                                             port=self._port,
                                             server=self._server)
        if isinstance(self.buffer, CommBufferSingleton):
            print("Sending commands directly to LCS Ser2...")
            print(f"Listening for client connections on port {self._args.server_port}...")
            self.receiver_thread = EnqueueProxyRequests(self.buffer, self._args.server_port)
        else:
            print(f"Sending commands to Proxy at {self._server}:{self._port}...")
        self.run()

    @property
    def buffer(self) -> CommBuffer:
        return self._comm_buffer

    def run(self) -> None:
        # configure command buffer
        # print opening line
        print(f"PyLegacy train controller, Ver 0.1")
        while True:
            try:
                ui: str = input(">> ")
                readline.add_history(ui)
                self._handle_command(ui)
            except SystemExit:
                pass
            except argparse.ArgumentError:
                pass
            except KeyboardInterrupt:
                self._comm_buffer.shutdown()
                break

    def _handle_command(self, ui: str) -> None:
        """
            Parse the user's input, reusing the individual CLI command parsers.
            If a valid command is specified, send it to the Lionel LCS SER2.
        """
        if ui is None:
            return
        ui = ui.lower().strip()
        if ui:
            # the argparse library requires the argument string to be presented as a list
            ui_parts = ui.split()
            if ui_parts[0]:
                # parse the first token
                try:
                    # if the keyboard input starts with a valid command, args.command
                    # is set to the corresponding CLI command class, or the verb 'quit'
                    args = self._command_parser().parse_args(['-' + ui_parts[0]])
                    if args.command == 'quit':
                        raise KeyboardInterrupt()
                    ui_parser = args.command.command_parser()
                    ui_parser.remove_args(['baudrate', 'port', 'server'])
                    cmd = args.command(ui_parser, ui_parts[1:], False).command
                    if cmd is None:
                        return
                    cmd.send(buffer=self.buffer)
                except argparse.ArgumentError:
                    print(f"'{ui}' is not a valid command")
                    return

    @staticmethod
    def _command_parser() -> ArgumentParser:
        """
            Parse the first token of the user's input
        """
        command_parser = ArgumentParser(add_help=False, exit_on_error=False)
        group = command_parser.add_mutually_exclusive_group()
        group.add_argument("-accessory",
                           action="store_const",
                           const=AccCli,
                           dest="command")
        group.add_argument("-engine",
                           action="store_const",
                           const=EngineCli,
                           dest="command")
        group.add_argument("-halt",
                           action="store_const",
                           const=HaltCli,
                           dest="command")
        group.add_argument("-lighting",
                           action="store_const",
                           const=LightingCli,
                           dest="command")
        group.add_argument("-route",
                           action="store_const",
                           const=RouteCli,
                           dest="command")
        group.add_argument("-switch",
                           action="store_const",
                           const=SwitchCli,
                           dest="command")
        group.add_argument("-quit",
                           action="store_const",
                           const="quit",
                           dest="command")
        return command_parser


if __name__ == '__main__':
    parser = ArgumentParser("Send TMCC and Legacy-formatted commands to a LCS SER2",
                            parents=[cli_parser()])
    parser.add_argument("-sp", "--server_port",
                        type=int,
                        default=DEFAULT_SERVER_PORT,
                        help=f"Port to use for remote connections, if client (default: {DEFAULT_SERVER_PORT})")
    TrainControl(parser.parse_args())
