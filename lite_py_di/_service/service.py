from .._container.container import Container
from ..config import ServiceConfig

def service(service_config: ServiceConfig | None = None):
    """Decorator for registering a class as a dependency in the Container.
    Args:
        is_singleton (bool, optional): Indicates whether the dependency should be a singleton.
            Defaults to True.
    """

    if service_config is None:
        service_config = ServiceConfig()

    def decorator(cls):
        Container().register(cls, service_config)
        
        return cls
    
    return decorator
