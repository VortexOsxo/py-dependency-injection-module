from dataclasses import dataclass

@dataclass
class _RegisterConfig:
    class_type: type
    is_singleton: bool
