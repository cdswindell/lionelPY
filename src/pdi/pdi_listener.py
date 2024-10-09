from __future__ import annotations

import socket
import threading
from collections import deque, defaultdict
from queue import Queue
from threading import Thread
from typing import Tuple

from .constants import PDI_SOP, PDI_STF, PDI_EOP, PdiAction
from .pdi_req import PdiReq, TmccReq
from ..comm.command_listener import Topic, Message, Channel, Subscriber, CommandDispatcher
from ..comm.enqueue_proxy_requests import EnqueueProxyRequests
from ..protocol.constants import DEFAULT_QUEUE_SIZE, DEFAULT_BASE3_PORT, BROADCAST_TOPIC


class PdiListener(Thread):
    _instance: None = None
    _lock = threading.RLock()

    @classmethod
    def build(cls,
              base3: str,
              base3_port: int = DEFAULT_BASE3_PORT,
              queue_size: int = DEFAULT_QUEUE_SIZE) -> PdiListener:
        """
            Factory method to create a CommandListener instance
        """
        return PdiListener(base3, base3_port, queue_size)

    @classmethod
    def listen_for(cls,
                   listener: Subscriber,
                   channel: Topic,
                   address: int = None,
                   action: PdiAction = None):
        if cls._instance is not None:
            cls._instance.dispatcher.subscribe(listener, channel, address, action)
        else:
            raise AttributeError("Pdi Listener not initialized")

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def is_built(cls) -> bool:
        return cls._instance is not None

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def is_running(cls) -> bool:
        # noinspection PyProtectedMember
        return cls._instance is not None and cls._instance._is_running

    @classmethod
    def enqueue_command(cls, data: bytes | PdiReq) -> None:
        if cls._instance is not None and data:
            if isinstance(data, PdiReq):
                data = data.as_bytes
            # noinspection PyProtectedMember
            cls._instance._base3.send(data)

    @classmethod
    def stop(cls) -> None:
        with cls._lock:
            if cls._instance:
                cls._instance.shutdown()

    def __new__(cls, *args, **kwargs):
        """
            Provides singleton functionality. We only want one instance
            of this class in a process
        """
        with cls._lock:
            if PdiListener._instance is None:
                PdiListener._instance = super(PdiListener, cls).__new__(cls)
                PdiListener._instance._initialized = False
            return PdiListener._instance

    def __init__(self,
                 base3_addr: str,
                 base3_port: int = DEFAULT_BASE3_PORT,
                 queue_size: int = DEFAULT_QUEUE_SIZE) -> None:
        if self._initialized:
            return
        else:
            self._initialized = True
        self._base3_addr = base3_addr
        self._base3_port = base3_port
        super().__init__(daemon=True, name="PyLegacy PDI Listener")

        # open a connection to our Base 3
        from .base3_buffer import Base3Buffer
        self._base3 = Base3Buffer(base3_addr, base3_port, queue_size, self)

        # create the thread

        # prep our consumer(s)
        self._cv = threading.Condition()
        self._deque = deque(maxlen=DEFAULT_QUEUE_SIZE)
        self._is_running = True
        self._dispatcher = PdiDispatcher.build(queue_size)

        # start listener thread
        self.start()

    @property
    def dispatcher(self) -> PdiDispatcher:
        return self._dispatcher

    def run(self) -> None:
        while self._is_running:
            # process bytes, as long as there are any
            with self._cv:
                if not self._deque:
                    self._cv.wait()  # wait to be notified
            # check if the first bite is in the list of allowable command prefixes
            dq_len = len(self._deque)
            while dq_len > 0:  # may indicate thread is exiting
                # we now begin a state machine where we look for an SOP/EOP pair. Throw away
                # bytes until we see an SOP
                if self._deque[0] == PDI_SOP:
                    # we've found the possible start of a PDI command sequence. Check if we've found
                    # a PDI_EOP byte, or a "stuff" byte; we handle each situation separately
                    try:
                        eop_pos = self._deque.index(PDI_EOP)
                    except ValueError:
                        # no luck, wait for more bytes; should we impose a maximum byte count?
                        dq_len = -1  # to bypass inner while loop; we need more data
                        continue
                    # make sure preceding byte isn't a stuff byte
                    if eop_pos - 1 > 0:
                        if self._deque[eop_pos - 1] == PDI_STF:
                            print("*** we found an unhandled stuff-it")
                            continue  # this isn't really an EOF
                        # we found a complete PDI packet! Queue it for processing
                        req_bytes = bytes()
                        for _ in range(eop_pos + 1):
                            req_bytes += self._deque.popleft().to_bytes(1, byteorder='big')
                            dq_len -= 1
                        try:
                            self._dispatcher.offer(PdiReq.from_bytes(req_bytes))
                        except Exception as e:
                            print(f"Failed to dispatch request {req_bytes.hex(':')}: {e}")
                        continue  # with while dq_len > 0 loop
                # pop this byte and continue; we either received unparsable input
                # or started receiving data mid-command
                print(f"Ignoring {hex(self._deque.popleft())}")
                dq_len -= 1
        # shut down the dispatcher
        if self._dispatcher:
            self._dispatcher.shutdown()

    def offer(self, data: bytes) -> None:
        if data:
            with self._cv:
                self._deque.extend(data)
                self._cv.notify()

    def shutdown(self) -> None:
        if hasattr(self, "_cv"):
            with self._cv:
                self._is_running = False
                self._cv.notify()
        if hasattr(self, "_dispatcher"):
            if self._dispatcher:
                self._dispatcher.shutdown()
        if hasattr(self, "_base3"):
            if self._base3:
                self._base3.shutdown()
        PdiListener._instance = None

    def subscribe(self,
                  listener: Subscriber,
                  channel: Topic,
                  address: int = None,
                  action: PdiAction = None) -> None:
        self._dispatcher.subscribe(listener, channel, address, action)

    def unsubscribe(self,
                    listener: Subscriber,
                    channel: Topic,
                    address: int = None,
                    action: PdiAction = None) -> None:
        self._dispatcher.unsubscribe(listener, channel, address, action)

    def subscribe_any(self, subscriber: Subscriber) -> None:
        self._dispatcher.subscribe_any(subscriber)

    def unsubscribe_any(self, subscriber: Subscriber) -> None:
        self._dispatcher.unsubscribe_any(subscriber)


class PdiDispatcher(Thread):
    """
        The PdiDispatcher thread receives parsed PdiReqs from the
        PdiListener and dispatches them to subscribing listeners
    """
    _instance = None
    _lock = threading.RLock()

    @classmethod
    def build(cls, queue_size: int = DEFAULT_QUEUE_SIZE) -> PdiDispatcher:
        """
            Factory method to create a CommandDispatcher instance
        """
        return PdiDispatcher(queue_size)

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def is_running(cls) -> bool:
        # noinspection PyProtectedMember
        return cls._instance is not None and cls._instance._is_running

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def is_built(cls) -> bool:
        return cls._instance is not None

    def __new__(cls, *args, **kwargs):
        """
            Provides singleton functionality. We only want one instance
            of this class in a process
        """
        with cls._lock:
            if PdiDispatcher._instance is None:
                PdiDispatcher._instance = super(PdiDispatcher, cls).__new__(cls)
                PdiDispatcher._instance._initialized = False
            return PdiDispatcher._instance

    def __init__(self, queue_size: int = DEFAULT_QUEUE_SIZE) -> None:
        if self._initialized:
            return
        else:
            self._initialized = True
        super().__init__(daemon=True, name="PyLegacy Pdi Dispatcher")
        self._channels: dict[Topic | Tuple[Topic, int], Channel[Message]] = defaultdict(Channel)
        self._cv = threading.Condition()
        self._is_running = True
        self._broadcasts = False
        self._queue = Queue[PdiReq](queue_size)
        self._tmcc_dispatcher = CommandDispatcher.get()
        self._client_port = EnqueueProxyRequests.port if EnqueueProxyRequests.is_built else None
        self.start()

    @property
    def broadcasts_enabled(self) -> bool:
        return self._broadcasts

    def run(self) -> None:
        while self._is_running:
            with self._cv:
                if self._queue.empty():
                    self._cv.wait()
            if self._queue.empty():  # we need to do a second check in the event we're being shutdown
                continue
            cmd: PdiReq = self._queue.get()
            try:
                # publish dispatched pdi commands to listeners
                if isinstance(cmd, PdiReq):
                    # for TMCC requests, forward to CommandListener
                    if isinstance(cmd, TmccReq):
                        self._tmcc_dispatcher.offer(cmd.tmcc_command)
                    else:
                        self.publish((cmd.scope, cmd.tmcc_id, cmd.action), cmd)
                        self.publish((cmd.scope, cmd.tmcc_id), cmd)
                        self.publish(cmd.scope, cmd)
                    if self._broadcasts:
                        self.publish(BROADCAST_TOPIC, cmd)
                    if self._client_port is not None:
                        self.update_client_state(cmd)
            except Exception as e:
                print(e)
            finally:
                self._queue.task_done()

    def update_client_state(self, command: PdiReq):
        """
            Update all PyTrain clients with the dispatched command. Used to keep
            client states in sync with server
        """
        if self._client_port is not None:
            # noinspection PyTypeChecker
            for client in EnqueueProxyRequests.clients:
                try:
                    with self._lock:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((client, self._client_port))
                            s.sendall(command.as_bytes)
                            _ = s.recv(16)
                except ConnectionRefusedError:
                    # ignore disconnects; client will receive state update on reconnect
                    pass
                except Exception as e:
                    print(f"Exception while sending PDI state update to {client}: {e}")

    def offer(self, pdi_req: PdiReq) -> None:
        """
            Receive a command from the listener thread and dispatch it to subscribers.
            We do this in a separate thread so that the listener thread doesn't fall behind
        """
        if pdi_req is not None and isinstance(pdi_req, PdiReq) and not pdi_req.is_ping:
            with self._cv:
                self._queue.put(pdi_req)
                self._cv.notify()  # wake up receiving thread

    def shutdown(self) -> None:
        with self._cv:
            self._is_running = False
            self._cv.notify()
        PdiDispatcher._instance = None

    @staticmethod
    def _make_channel(channel: Topic,
                      address: int = None,
                      action: PdiAction = None) -> Topic | Tuple:
        if channel is None:
            raise ValueError("Channel required")
        elif address is None:
            return channel
        elif action is None:
            return channel, address
        else:
            return channel, address, action

    def publish(self, channel: Topic, message: Message) -> None:
        if channel in self._channels:  # otherwise, we would create a channel simply by referencing i
            self._channels[channel].publish(message)

    def subscribe(self,
                  subscriber: Subscriber,
                  channel: Topic,
                  address: int = None,
                  action: PdiAction = None) -> None:
        if channel == BROADCAST_TOPIC:
            self.subscribe_any(subscriber)
        else:
            self._channels[self._make_channel(channel, address, action)].subscribe(subscriber)

    def unsubscribe(self,
                    subscriber: Subscriber,
                    channel: Topic,
                    address: int = None,
                    command: PdiAction = None) -> None:
        if channel == BROADCAST_TOPIC:
            self.unsubscribe_any(subscriber)
        else:
            channel = self._make_channel(channel, address, command)
            self._channels[channel].unsubscribe(subscriber)
            if len(self._channels[channel].subscribers) == 0:
                del self._channels[channel]

    def subscribe_any(self, subscriber: Subscriber) -> None:
        # receive broadcasts
        self._channels[BROADCAST_TOPIC].subscribe(subscriber)
        self._broadcasts = True

    def unsubscribe_any(self, subscriber: Subscriber) -> None:
        # receive broadcasts
        self._channels[BROADCAST_TOPIC].unsubscribe(subscriber)
        if not self._channels[BROADCAST_TOPIC].subscribers:
            self._broadcasts = False
