from dataclasses import dataclass, field

@dataclass
class ServiceConfig:
    is_singleton: bool = field(default=True)
