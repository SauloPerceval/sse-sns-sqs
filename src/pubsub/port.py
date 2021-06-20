from abc import ABC, abstractmethod
from typing import Optional, Generator


class MessageAnnouncer(ABC):
    @abstractmethod
    def listen(self, channel="default") -> 'Listener':
        raise NotImplementedError

    def announce(self, data: str, event=None, channel="default") -> None:
        def format_sse(data: str, event=None) -> str:
            msg = f'data: {data}\n\n'
            if event is not None:
                msg = f'event: {event}\n{msg}'
            return msg

        self.announce_formatted(formatted_msg=format_sse(data=data, event=event),
                                channel=channel)

    @abstractmethod
    def announce_formatted(self, formatted_msg: str, channel="default") -> None:
        raise NotImplementedError


class Listener(ABC):
    @abstractmethod
    def messages_generator(self) -> Generator[str, None, None]:
        raise NotImplementedError
