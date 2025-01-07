from .._container.container import Container
from ..config import ServiceConfig

def service(argument: ServiceConfig | type | None  = None):
    """Decorator for registering a class as a dependency in the Container.
    Args:
        argument (ServiceConfig | type | None, optional): Can either be a configuration for the service, or the class itself to use the default configuration.
    """
    if isinstance(argument, type):
        Container().register(argument, ServiceConfig())
        return argument

    service_config = ServiceConfig() if argument is None else argument

    def decorator(cls):
        Container().register(cls, service_config)
        
        return cls
    
    return decorator
