from dataclasses import dataclass, field
from ..config import ServiceConfig

@dataclass
class _RegisterConfig(ServiceConfig):
    class_type: type = field(default=None)
