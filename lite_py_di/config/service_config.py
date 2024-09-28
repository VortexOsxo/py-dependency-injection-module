from dataclasses import dataclass, field

@dataclass
class ServiceConfig:
    """
    Configuration for a service in the dependency injection container.

    Attributes:
        is_singleton (bool): Indicates if the service is a singleton. Defaults to True.
        is_loaded_eagerly (bool): Indicates if the service is loaded eagerly (loaded on container initialization) or lazily (loaded on first access). Defaults to False.
    """
    is_singleton: bool = field(default=True)
    is_loaded_eagerly: bool = field(default=False)
