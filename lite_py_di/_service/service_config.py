from dataclasses import dataclass

@dataclass
class ServiceConfig:
    class_type: type
    is_singleton: bool
