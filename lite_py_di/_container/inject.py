from functools import wraps
from inspect import signature
from .container import Container

def inject(**injected_kwargs):
    """
    A decorator to inject services into a function's arguments based on the provided keyword arguments.
    The injected services must be the last parameters specified in the function signature.

    Args:
        **injected_kwargs: 
            - `param_name` (str): The name of the parameter to inject.
            - `lookup_value` (type | str): The type or name of the service to look up in the container.

    Returns:
        Callable
            A decorated function with injected services.

    Example:
        @inject(service=MyService)
        def my_function(other_param, default_param=0, service=None):
            pass
    """
    def decorator(func):
        new_sig = _get_updated_signature(func, injected_kwargs)

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs.update(_get_injected_services(injected_kwargs))
            return func(*args, **kwargs)
        
        wrapper.__signature__ = new_sig
        return wrapper
    return decorator

def _get_updated_signature(func, injected_kwargs):
    original_sig = signature(func)
        
    new_params = [
        param for param_name, param in original_sig.parameters.items()
        if param_name not in injected_kwargs
    ]
    return original_sig.replace(parameters=new_params)

def _get_injected_services(injected_kwargs):
    injected_services = {}

    for param_name, lookup_value in injected_kwargs.items():
        injected_services[param_name] = Container.get(lookup_value)
    
    return injected_services