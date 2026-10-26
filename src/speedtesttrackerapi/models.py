"""Data Models for the SpeedtestTrackerAPI Package."""

from datetime import date, datetime
from typing import Any, List, Literal, Optional, Union

from pydantic import AliasChoices, AnyUrl, BaseModel, ConfigDict, Field
from pydantic.networks import IPvAnyAddress


class BaseAPIModel(BaseModel):
    """Base model with permissive handling for the live API payloads."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class Ping(BaseAPIModel):
    """Ping data nested in a speedtest result."""

    low: Optional[float] = None
    high: Optional[float] = None
    jitter: Optional[float] = None
    latency: Optional[float] = None
    avg: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None


class DataResult(BaseAPIModel):
    """Result metadata nested in a speedtest payload."""

    id: Optional[Union[str, int]] = None
    url: Optional[AnyUrl] = None
    persisted: Optional[bool] = None


class Server(BaseAPIModel):
    """Server metadata used both in result payloads and the Ookla list."""

    id: Optional[int] = None
    ip: Optional[Union[str, IPvAnyAddress]] = None
    host: Optional[str] = None
    name: Optional[str] = None
    port: Optional[int] = None
    country: Optional[str] = None
    location: Optional[str] = None


class Latency(BaseAPIModel):
    """Latency stats nested in upload/download payloads."""

    iqm: Optional[float] = None
    low: Optional[float] = None
    high: Optional[float] = None
    jitter: Optional[float] = None


class Upload(BaseAPIModel):
    """Upload section of the speedtest payload."""

    bytes: Optional[int] = None
    elapsed: Optional[int] = None
    latency: Optional[Latency] = None
    bandwidth: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("bandwidth", "bandwith"),
    )


class Download(BaseAPIModel):
    """Download section of the speedtest payload."""

    bytes: Optional[int] = None
    elapsed: Optional[int] = None
    latency: Optional[Latency] = None
    bandwidth: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("bandwidth", "bandwith"),
    )


class Interface(BaseAPIModel):
    """Network interface details inside a result payload."""

    name: Optional[str] = None
    is_vpn: Optional[bool] = None
    mac_address: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("mac_address", "macAddress", "macAdrr", "mac"),
    )
    external_ip: Optional[Union[str, IPvAnyAddress]] = Field(
        default=None,
        validation_alias=AliasChoices("external_ip", "externalIp", "external_ip"),
    )
    internal_ip: Optional[Union[str, IPvAnyAddress]] = Field(
        default=None,
        validation_alias=AliasChoices("internal_ip", "internalIp", "internal_ip"),
    )


class ResultData(BaseAPIModel):
    """Nested data payload returned by a result record."""

    type: Optional[str] = None
    level: Optional[str] = None
    message: Optional[str] = None
    isp: Optional[str] = None
    ping: Optional[Ping] = None
    result: Optional[DataResult] = None
    server: Optional[Server] = None
    upload: Optional[Upload] = None
    download: Optional[Download] = None
    interface: Optional[Interface] = None
    timestamp: Optional[datetime] = None
    packet_loss: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("packet_loss", "packetLoss"),
    )


class Result(BaseAPIModel):
    """Speedtest result entry from the API."""

    id: Optional[int] = None
    service: Optional[str] = None
    ping: Optional[float] = None
    download: Optional[Union[int, float]] = None
    upload: Optional[Union[int, float]] = None
    download_bits: Optional[Union[int, float]] = None
    upload_bits: Optional[Union[int, float]] = None
    download_bits_human: Optional[str] = None
    upload_bits_human: Optional[str] = None
    download_bytes: Optional[Union[int, float]] = None
    upload_bytes: Optional[Union[int, float]] = None
    download_bytes_human: Optional[str] = None
    upload_bytes_human: Optional[str] = None
    benchmarks: Optional[dict] = None
    healthy: Optional[bool] = None
    status: Optional[str] = None
    scheduled: Optional[bool] = None
    dispatched_by: Optional[int] = None
    comments: Optional[str] = None
    data: Optional[ResultData] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ResultResponse(BaseAPIModel):
    """Response for a single Speedtest result entry."""

    data: Optional[Result] = None
    message: Optional[str] = None


class Links(BaseAPIModel):
    """Top-level pagination links on the paginated results response."""

    first: Optional[str] = None
    last: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None


class MetaLinks(BaseAPIModel):
    """Pagination items used inside meta.links."""

    url: Optional[str] = None
    label: Optional[str] = None
    page: Optional[int] = None
    active: Optional[bool] = None


class Meta(BaseAPIModel):
    """Meta data nested in the results collection."""

    current_page: Optional[int] = None
    from_: Optional[int] = Field(default=None, alias="from")
    last_page: Optional[int] = None
    links: Optional[List[MetaLinks]] = None
    path: Optional[str] = None
    per_page: Optional[int] = Field(default=None, alias="per.page")
    to: Optional[int] = None
    total: Optional[int] = None


class ResultsCollection(BaseAPIModel):
    """Paginated list of Speedtest results."""

    data: Optional[List[Result]] = None
    links: Optional[Links] = None
    meta: Optional[Meta] = None


class ServersCollection(BaseAPIModel):
    """Collection of Ookla speedtest servers."""

    data: Optional[List[Server]] = None
    message: Optional[str] = None


class SpeedtestRun(BaseAPIModel):
    """A queued speedtest result."""

    data: Optional[Result] = None
    message: Optional[str] = None


class PingStats(BaseAPIModel):
    """Aggregate ping statistics returned by /api/v1/stats."""

    avg: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None


class TransferStats(BaseAPIModel):
    """Aggregate transfer statistics returned by /api/v1/stats."""

    avg: Optional[float] = None
    avg_bits: Optional[int] = None
    avg_bits_human: Optional[str] = None
    min: Optional[float] = None
    min_bits: Optional[int] = None
    min_bits_human: Optional[str] = None
    max: Optional[float] = None
    max_bits: Optional[int] = None
    max_bits_human: Optional[str] = None


class StatsData(BaseAPIModel):
    """Nested aggregate statistics payload."""

    ping: Optional[PingStats] = None
    download: Optional[TransferStats] = None
    upload: Optional[TransferStats] = None
    total_results: Optional[int] = None


class Stats(BaseAPIModel):
    """Aggregated speedtest statistics response."""

    data: Optional[StatsData] = None
    message: Optional[str] = None


class QueryParameters(BaseAPIModel):
    """Query Parameters."""

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
