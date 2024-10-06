from __future__ import annotations

import socketserver
import threading
from threading import Thread
from typing import List

from src.comm.comm_buffer import CommBuffer
from src.protocol.constants import DEFAULT_SERVER_PORT

REGISTER_REQUEST: bytes = int(0xff).to_bytes(1) * 6
SYNC_STATE_REQUEST: bytes = int(0xfff0).to_bytes(2, byteorder='big') * 3


class EnqueueProxyRequests(Thread):
    """
        Receives requests from PyTrain clients over TCP/IP and queues them for
        dispatch to the LCS SER2.
    """
    _instance = None
    _lock = threading.RLock()

    @classmethod
    def build(cls, buffer: CommBuffer, port: int = DEFAULT_SERVER_PORT) -> EnqueueProxyRequests:
        """
            Factory method to create a EnqueueProxyRequests instance
        """
        return EnqueueProxyRequests(buffer, port)

    @classmethod
    def note_client_addr(cls, client: str) -> None:
        """
            Take note of client IPs, so we can update them of component state changes
        """
        if cls._instance is not None:
            # noinspection PyProtectedMember
            cls._instance._clients.add(client)

    @classmethod
    def get_comm_buffer(cls) -> CommBuffer:
        # noinspection PyProtectedMember
        return cls._instance._buffer if cls._instance is not None else None

    @classmethod
    def stop(cls) -> None:
        if cls._instance is not None:
            cls._instance.shutdown()

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def register_request(cls) -> bytes:
        return REGISTER_REQUEST

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def sync_state_request(cls) -> bytes:
        return SYNC_STATE_REQUEST

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def is_built(cls) -> bool:
        return cls._instance is not None

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def clients(cls) -> List[str]:
        # noinspection PyProtectedMember
        return list(cls._instance._clients)

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def port(cls) -> int:
        if cls._instance is not None:
            # noinspection PyProtectedMember
            return cls._instance._port
        raise AttributeError("EnqueueProxyRequests is not built yet.")

    def __init__(self,
                 buffer: CommBuffer,
                 port: int = DEFAULT_SERVER_PORT
                 ) -> None:
        if self._initialized:
            return
        else:
            self._initialized = True
        super().__init__(daemon=True, name="PyLegacy Enqueue Receiver")
        self._buffer: CommBuffer = buffer
        self._port = port
        self._clients: set[str] = set()
        self.start()

    def __new__(cls, *args, **kwargs):
        """
            Provides singleton functionality. We only want one instance
            of this class in the system
        """
        with cls._lock:
            if EnqueueProxyRequests._instance is None:
                EnqueueProxyRequests._instance = super(EnqueueProxyRequests, cls).__new__(cls)
                EnqueueProxyRequests._instance._initialized = False
            return EnqueueProxyRequests._instance

    def run(self) -> None:
        """
            Simplified TCP/IP Server listens for command requests from client and executes them
            on the PyTrain server.
        """
        # noinspection PyTypeChecker
        with socketserver.TCPServer(('', self._port), EnqueueHandler) as server:
            server.serve_forever()

    def shutdown(self) -> None:
        # noinspection PyTypeChecker
        with socketserver.TCPServer(('', self._port), EnqueueHandler) as server:
            server.shutdown()


class EnqueueHandler(socketserver.BaseRequestHandler):
    def handle(self):
        byte_stream = bytes()
        while True:
            data = self.request.recv(128)
            if data:
                byte_stream += data
                self.request.sendall(str.encode("ack"))
            else:
                break
        EnqueueProxyRequests.note_client_addr(self.client_address[0])
        if data == EnqueueProxyRequests.register_request:
            pass
        elif data == EnqueueProxyRequests.sync_state_request:
            pass
        else:
            EnqueueProxyRequests.get_comm_buffer().enqueue_command(byte_stream)
