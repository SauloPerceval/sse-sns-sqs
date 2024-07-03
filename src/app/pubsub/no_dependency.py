import queue
from typing import Generator

from app.pubsub.port import MessageAnnouncer, Listener


class NoDepMessageAnnouncer(MessageAnnouncer):
    def __init__(self):
        self.listeners = []

    def listen(self, channel="default") -> 'NoDepListener':
        q = queue.Queue(maxsize=5)
        self.listeners.append({channel: q})
        return NoDepListener(listener_queue=q)

    def announce_formatted(self, formatted_msg: str, channel="default") -> None:
        for listener in self.listeners:
            try:
                listener_queue = listener.get(channel)
                if listener_queue:
                    listener_queue.put_nowait(formatted_msg)
            except queue.Full:
                self.listeners.remove(listener)


class NoDepListener(Listener):
    def __init__(self, listener_queue: queue.Queue):
        self.listener_queue = listener_queue

    def messages_generator(self) -> Generator[str, None, None]:
        while True:
            yield self.listener_queue.get()
