import queue
from typing import Dict, Generator, List

from app.pubsub.port import MessageAnnouncer, Listener


class NoDepMessageAnnouncer(MessageAnnouncer):
    def __init__(self):
        self.listeners_channels: Dict[str, List[queue.Queue]] = {}

    def listen(self, channel="default") -> 'NoDepListener':
        q = queue.Queue(maxsize=5)
        
        listeners_channel = self.listeners_channels.get(channel)
        
        if listeners_channel is None:
            self.listeners_channels[channel] = [q]
        
        else:
            listeners_channel.append(q)
        
        return NoDepListener(listener_queue=q)

    def announce_formatted(self, formatted_msg: str, channel="default") -> None:
        listeners_channel = self.listeners_channels.get(channel, [])
        
        for listener_queue in listeners_channel:
            try:
                listener_queue.put_nowait(formatted_msg)
            except queue.Full:
                listeners_channel.remove(listener_queue)
                
                if len(listeners_channel) == 0:
                    del self.listeners_channels[channel]


class NoDepListener(Listener):
    def __init__(self, listener_queue: queue.Queue):
        self.listener_queue = listener_queue

    def messages_generator(self) -> Generator[str, None, None]:
        while True:
            yield self.listener_queue.get()
