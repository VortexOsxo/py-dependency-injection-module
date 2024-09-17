from dataclasses import dataclass

@dataclass
class DependencyConfig:
    class_type: type
    is_singleton: bool
