from asyncio import transports
from asyncio.protocols import Protocol
from typing import Optional


class TcpProtocal(Protocol):

    def eof_received(self) -> Optional[bool]:
        pass

    def data_received(self, data: bytes) -> None:
        pass

    def connection_made(self, transport: transports.BaseTransport) -> None:
        pass

    def connection_lost(self, exc: Optional[Exception]) -> None:
        pass
