from ..container.container import Container

def dependency(is_singleton=True):
    """Decorator for registering a class as a dependency in the Container.
    Args:
        is_singleton (bool, optional): Indicates whether the dependency should be a singleton.
            Defaults to True.
    """
    def decorator(cls):
        Container().register(cls, is_singleton)
        return cls
    
    return decorator
