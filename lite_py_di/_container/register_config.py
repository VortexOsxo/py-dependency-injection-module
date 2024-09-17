from dataclasses import dataclass

@dataclass
class RegisterConfig:
    class_type: type
    is_singleton: bool
