from __future__ import annotations

import abc
from abc import ABC
from typing import Self, Tuple, TypeVar

from .constants import PDI_SOP, PDI_EOP, PdiCommand, PDI_STF, CommonAction, PdiAction
from .constants import IrdaAction, Ser2Action
from ..protocol.command_req import CommandReq
from ..protocol.constants import CommandScope

T = TypeVar('T', bound=PdiAction)

DEVICE_TO_REQ_MAP = {}


class PdiReq(ABC):
    __metaclass__ = abc.ABCMeta

    # noinspection PyUnresolvedReferences
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        from src.pdi.asc2_req import Asc2Req
        from src.pdi.bpc2_req import Bpc2Req
        from src.pdi.wifi_req import WiFiReq

        # throws an exception if we can't dereference
        pdi_cmd = PdiCommand(data[1])

        dev_type = pdi_cmd.name.split('_')[0].upper()
        if dev_type in DEVICE_TO_REQ_MAP:
            return DEVICE_TO_REQ_MAP[dev_type](data)
        else:
            raise NotImplementedError(f"PdiCommand {pdi_cmd.name} not implemented")

    def __init__(self,
                 data: bytes | None,
                 pdi_command: PdiCommand = None) -> None:
        if isinstance(data, bytes):
            # first byte should be SOP, last should be EOP, if not, raise exception
            if data[0] != PDI_SOP or data[-1] != PDI_EOP:
                raise ValueError(f"Invalid PDI Request: {data}")
            # process the data to remove SOP, EOP, Checksum, and Stuff Bytes, if any
            self._original = data
            recv_checksum = data[-2]
            self._data, check_sum = self._calculate_checksum(data[1:-2], False)
            if recv_checksum != int.from_bytes(check_sum):
                raise ValueError(f"Invalid PDI Request: {data}  [BAD CHECKSUM]")
            self._pdi_command: PdiCommand = PdiCommand(data[1])
        else:
            if pdi_command is None or not isinstance(pdi_command, PdiCommand):
                raise ValueError(f"Invalid PDI Request: {pdi_command}")
            self._pdi_command = pdi_command
            self._data = self._original = None

    def __repr__(self) -> str:
        data = f" (0x{self._data.hex()})" if self._data is not None else " 0x" + self.as_bytes.hex()
        return f"[PDI {self._pdi_command.friendly}{data}]"

    @staticmethod
    def _calculate_checksum(data: bytes, add_stf=True) -> Tuple[bytes, bytes]:
        byte_stream = bytes()
        check_sum = 0
        for b in data:
            check_sum += b
            if b in [PDI_SOP, PDI_STF, PDI_EOP]:
                check_sum += PDI_STF
                if add_stf is True:
                    byte_stream += PDI_STF.to_bytes(1, byteorder='big')
                else:
                    continue
            byte_stream += b.to_bytes(1, byteorder='big')
        # do checksum calculation on buffer
        check_sum = 0xff & (0 - check_sum)
        return byte_stream, check_sum.to_bytes(1, byteorder='big')

    @property
    def pdi_command(self) -> PdiCommand:
        return self._pdi_command

    @property
    def tmcc_id(self) -> int:
        return 0

    @property
    def address(self) -> int:
        # for compatibility with state management system
        return self.tmcc_id

    @property
    def command(self) -> PdiCommand:
        # for compatibility with state management system
        return self.pdi_command

    @property
    def action(self) -> T | None:
        return None

    @property
    def as_bytes(self) -> bytes:
        """
            Default implementation, should override in more complex requests
        """
        byte_str = self.pdi_command.as_bytes
        byte_str += self.tmcc_id.to_bytes(1, byteorder='big')
        byte_str += CommonAction.CONFIG.as_bytes
        byte_str, checksum = self._calculate_checksum(byte_str)
        byte_str = PDI_SOP.to_bytes(1, byteorder='big') + byte_str
        byte_str += checksum
        byte_str += PDI_EOP.to_bytes(1, byteorder='big')
        byte_str = byte_str.upper()
        return byte_str

    @property
    def checksum(self) -> bytes:
        check_sum = 0
        for b in self._data:
            if b in [PDI_SOP, PDI_EOP]:
                continue
            check_sum += b
        check_sum = 0xFF & (0 - check_sum)
        return check_sum.to_bytes(1)

    @property
    def is_ping(self) -> bool:
        return self._pdi_command == PdiCommand.PING

    @property
    def is_tmcc(self) -> bool:
        return self._pdi_command.is_tmcc

    @property
    def payload(self) -> str | None:
        return f"({self.packet})"

    @property
    def packet(self) -> str:
        if self._data is None:
            return "0x" + self.as_bytes.hex()
        else:
            return "0x" + self._data.hex()

    @property
    @abc.abstractmethod
    def scope(self) -> CommandScope:
        ...


class LcsReq(PdiReq, ABC):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data: bytes | int,
                 pdi_command: PdiCommand = None,
                 action: int = None,
                 ident: int | None = None) -> None:
        super().__init__(data, pdi_command)
        if isinstance(data, bytes):
            if PdiCommand(data[1]).is_lcs is False:
                raise ValueError(f"Invalid PDI LCS Request: {data}")
            self._tmcc_id = self._data[1]
            self._action_byte = self._data[2]
            self._ident = None
        else:
            self._action_byte = action
            self._tmcc_id = int(data)
            self._ident = ident

    def __repr__(self) -> str:
        if self.payload is not None:
            payload = " " + self.payload
        elif self._data is not None:
            payload = f" (0x{self._data.hex()})" if self._data else ""
        else:
            payload = ""

        return f"[PDI {self._pdi_command.name} ID: {self._tmcc_id} {self.action.name}{payload}]"

    @property
    def tmcc_id(self) -> int:
        return self._tmcc_id

    @property
    def ident(self) -> int:
        return self._ident

    @property
    def as_bytes(self) -> bytes:
        byte_str = self.pdi_command.as_bytes
        byte_str += self.tmcc_id.to_bytes(1, byteorder='big')
        byte_str += self.action.as_bytes
        byte_str, checksum = self._calculate_checksum(byte_str)
        byte_str = PDI_SOP.to_bytes(1, byteorder='big') + byte_str
        byte_str += checksum
        byte_str += PDI_EOP.to_bytes(1, byteorder='big')
        return byte_str

    @property
    @abc.abstractmethod
    def action(self) -> T:
        ...


class Ser2Req(LcsReq):
    def __init__(self,
                 data: bytes | int,
                 pdi_command: PdiCommand = PdiCommand.SER2_GET,
                 action: Ser2Action = Ser2Action.CONFIG,
                 ident: int | None = None) -> None:
        super().__init__(data, pdi_command, action.bits, ident)
        if isinstance(data, bytes):
            self._action = Ser2Action(self._action_byte)
        else:
            self._action = action

    @property
    def action(self) -> Ser2Action:
        return self._action

    @property
    def payload(self) -> str | None:
        return None

    @property
    def scope(self) -> CommandScope:
        return CommandScope.SYSTEM


DEVICE_TO_REQ_MAP['SER2'] = Ser2Req


class IrdaReq(LcsReq):
    def __init__(self,
                 data: bytes | int,
                 pdi_command: PdiCommand = PdiCommand.IRDA_GET,
                 action: IrdaAction = IrdaAction.CONFIG,
                 ident: int | None = None) -> None:
        super().__init__(data, pdi_command, action.bits, ident)
        if isinstance(data, bytes):
            self._action = IrdaAction(self._action_byte)
        else:
            self._action = action

    @property
    def action(self) -> IrdaAction:
        return self._action

    @property
    def payload(self) -> str | None:
        return None

    @property
    def scope(self) -> CommandScope:
        return CommandScope.SYSTEM


DEVICE_TO_REQ_MAP['IRDA'] = IrdaReq


class TmccReq(PdiReq):
    def __init__(self,
                 data: bytes | CommandReq,
                 pdi_command: PdiCommand = None):
        super().__init__(data, pdi_command=pdi_command)
        if isinstance(data, CommandReq):
            if self.pdi_command.is_tmcc is False:
                raise ValueError(f"Invalid PDI TMCC Request: {self.pdi_command}")
            self._tmcc_command: CommandReq = data
        else:
            if PdiCommand(data[1]) not in [PdiCommand.TMCC_TX, PdiCommand.TMCC_RX]:
                raise ValueError(f"Invalid PDI TMCC Request: {data}")
            self._tmcc_command: CommandReq = CommandReq.from_bytes(self._data[1:])

    def __repr__(self) -> str:
        data = f" (0x{self._data.hex()})" if self._data else ""
        return f"[PDI {self._pdi_command.friendly} {self.tmcc_command}{data}]"

    @property
    def tmcc_command(self) -> CommandReq:
        return self._tmcc_command

    @property
    def as_bytes(self) -> bytes:
        byte_str = self.pdi_command.as_bytes + self.tmcc_command.as_bytes
        byte_str, checksum = self._calculate_checksum(byte_str)
        byte_str = PDI_SOP.to_bytes(1, byteorder='big') + byte_str
        byte_str += checksum
        byte_str += PDI_EOP.to_bytes(1, byteorder='big')
        return byte_str

    @property
    def scope(self) -> CommandScope:
        return CommandScope.SYSTEM


DEVICE_TO_REQ_MAP['TMCC'] = TmccReq


class BaseReq(PdiReq):
    def __init__(self, data: bytes):
        if PdiCommand(data[1]).is_base is False:
            raise ValueError(f"Invalid PDI Base Request: {data}")
        super().__init__(data)

    @property
    def scope(self) -> CommandScope:
        return CommandScope.SYSTEM


DEVICE_TO_REQ_MAP['BASE'] = BaseReq
DEVICE_TO_REQ_MAP['UPDATE'] = BaseReq


class AllGetReq(PdiReq):
    def __init__(self,
                 data: bytes = None,
                 pdi_command: PdiCommand = PdiCommand.ALL_GET) -> None:
        super().__init__(data, pdi_command)

    @property
    def payload(self) -> str | None:
        return None

    @property
    def scope(self) -> CommandScope:
        return CommandScope.SYSTEM


DEVICE_TO_REQ_MAP['ALL'] = AllGetReq


class PingReq(PdiReq):
    def __init__(self, data: bytes | None = None):
        super().__init__(data, PdiCommand.PING)
        if data is not None:
            if PdiCommand(data[1]).is_ping is False:
                raise ValueError(f"Invalid PDI Ping Request: {data}")

    @property
    def as_bytes(self) -> bytes:
        byte_str = self.pdi_command.as_bytes
        byte_str, checksum = self._calculate_checksum(byte_str)
        byte_str = PDI_SOP.to_bytes(1, byteorder='big') + byte_str
        byte_str += checksum
        byte_str += PDI_EOP.to_bytes(1, byteorder='big')
        return byte_str

    @property
    def scope(self) -> CommandScope:
        return CommandScope.SYSTEM

    def __repr__(self) -> str:
        return f"[PDI {self._pdi_command.friendly}]"


DEVICE_TO_REQ_MAP['PING'] = PingReq
