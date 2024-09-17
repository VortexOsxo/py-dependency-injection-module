from dataclasses import dataclass, field

@dataclass
class ServiceConfig:
    """
    Configuration for a service in the dependency injection container.

    Attributes:
        is_singleton (bool): Indicates if the service is a singleton. Defaults to True.
    """
    is_singleton: bool = field(default=True)
