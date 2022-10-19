import dataclasses


@dataclasses.dataclass
class NoaaMetadata:
    """HTTP response metadata from NOAA requests"""
    correlation_id: str
    request_id: str
    server_id: str
    edge_request_id: str


def parse(headers: dict) -> NoaaMetadata:
    """Parses NOAA metadata from a dict-like collection of HTTP headers"""
    return NoaaMetadata(
        correlation_id=headers.get("X-Correlation-ID", ""),
        request_id=headers.get("X-Request-ID", ""),
        server_id=headers.get("X-Server-ID", ""),
        edge_request_id=headers.get("X-Edge-Request-ID", "")
    )
