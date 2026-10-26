"""Data Models for the SpeedtestTrackerAPI Package"""

from pydantic import BaseModel, Field, AnyUrl, field_validator
from pydantic.networks import IPvAnyAddress
from datetime import datetime, date
from typing import List, Optional, Literal


class Ping(BaseModel):
    """Ping data nested in Data()"""

    low: Optional[float] = None
    high: Optional[float] = None
    jitter: Optional[float] = None
    latency: Optional[float] = None


class DataResult(BaseModel):
    """Result data nested in Data()"""

    id: Optional[str] = None
    url: Optional[AnyUrl] = None
    persisted: Optional[bool] = None


class Server(BaseModel):
    """Server data nested in Data()"""

    id: Optional[int] = None
    ip: Optional[IPvAnyAddress] = None
    host: Optional[str] = None
    name: Optional[str] = None
    port: Optional[int] = None
    country: Optional[str] = None
    location: Optional[str] = None


class Latency(BaseModel):
    """Latency data nested in Data()"""

    iqm: Optional[float] = None
    low: Optional[float] = None
    high: Optional[float] = None
    jitter: Optional[float] = None


class Upload(BaseModel):
    """Upload data nested in Data()"""

    bytes: Optional[int] = None
    elapsed: Optional[int] = None
    latency: Latency
    bandwith: Optional[int] = None


class Download(BaseModel):
    """Download data nested in Data()"""

    bytes: Optional[int] = None
    elapsed: Optional[int] = None
    latency: Latency
    bandwith: Optional[int] = None


class Interface(BaseModel):
    """Interface data nested in Data()"""

    name: Optional[str] = None
    is_vpn: Optional[bool] = None
    mac_address: Optional[str] = Field(
        alias="macAdrr", pattern=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", default=None
    )
    external_ip: Optional[IPvAnyAddress] = Field(alias="externalIp", default=None)
    internal_ip: Optional[IPvAnyAddress] = Field(alias="internalIp", default=None)


class Data(BaseModel):
    """Nested speedtest data payload"""

    isp: Optional[str] = None
    ping: Ping
    type: Optional[str] = None
    result: DataResult
    server: Server
    upload: Upload
    download: Download
    interface: Interface
    timestamp: Optional[datetime] = None
    packet_loss: Optional[float] = Field(alias="packetLoss", default=None)


class Result(BaseModel):
    """Speedtest result entry"""

    id: Optional[int] = None
    service: Optional[str] = None
    ping: Optional[int] = None
    download: Optional[int] = None
    upload: Optional[int] = None
    download_bits: Optional[int] = None
    upload_bits: Optional[int] = None
    download_bits_human: Optional[int] = None
    upload_bits_human: Optional[int] = None
    benchmarks: Optional[dict] = None
    healthy: Optional[bool] = None
    status: Optional[str] = None
    scheduled: Optional[bool] = None
    comments: Optional[str] = None
    data: Data
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ResultResponse(BaseModel):
    """Response for a single Speedtest result entry"""

    data: Result
    message: Optional[str] = None


class Links(BaseModel):
    """Links data nested in ResultsCollection()"""

    first: Optional[str] = None
    last: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None


class MetaLinks(BaseModel):
    """Links data nested in Meta()"""

    url: Optional[str] = None
    label: Optional[str] = None
    active: Optional[bool] = None


class Meta(BaseModel):
    """Meta data nested in ResultsCollection()"""

    current_page: Optional[int] = None
    from_: Optional[int] = Field(alias="from", default=None)
    last_page: Optional[int] = None
    links: MetaLinks
    path: Optional[str] = None
    per_page: Optional[int] = Field(alias="per.page", default=None)
    to: Optional[int] = None
    total: Optional[int] = None


class ResultsCollection(BaseModel):
    """Paginated list of Speedtest results"""

    data: Optional[List[Result]] = None
    links: Links
    meta: Meta


class ServersCollection(BaseModel):
    """Collection of Ookla speedtest servers"""

    data: Optional[List[Server]] = None
    message: Optional[str] = None


class SpeedtestRun(BaseModel):
    """A queued speedtest result"""

    data: Result
    message: Optional[str] = None


class Stats(BaseModel):
    """Aggregated speedtest statistics"""

    total_results: Optional[int] = None
    avg_ping: Optional[float] = None
    avg_upload: Optional[float] = None
    avg_download: Optional[float] = None
    min_ping: Optional[float] = None
    min_download: Optional[float] = None
    min_upload: Optional[float] = None
    max_ping: Optional[float] = None
    max_download: Optional[float] = None
    max_upload: Optional[float] = None


class QueryParameters(BaseModel):
    """Query Parameters"""

    per_page: Optional[int] = Field(alias="per.page", ge=1, le=500, default=25)
    ping_filter: Optional[int] = Field(alias="filter[ping]", default=None)
    download_filter: Optional[int] = Field(alias="filter[download]", default=None)
    upload_filter: Optional[int] = Field(alias="filter[upload]", default=None)
    health_filter: Optional[bool] = Field(alias="filter[healthy]", default=None)
    status_filter: Optional[str] = Field(alias="filter[status]", default=None)
    scheduled_filter: Optional[bool] = Field(alias="filter[scheduled]", default=None)
    start_at_filter: Optional[date] = Field(alias="filter[start_at]", default=None)
    end_at_filter: Optional[date] = Field(alias="filter[end_at]", default=None)
    sort: Optional[
        Literal[
            "ping",
            "-ping",
            "download",
            "-download",
            "upload",
            "-upload",
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
        ]
    ] = None
    server_id: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
