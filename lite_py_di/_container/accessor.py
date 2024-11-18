from inspect import signature
from functools import wraps
from lite_py_di._container.inject import _get_injected_services, _get_updated_signature

def accessor(cls):
    init_signature = signature(cls.__init__)
    injected_kwargs = {}

    for parameter_name, parameter in init_signature.parameters.items():
        param_type = parameter.annotation if parameter.annotation is not parameter.empty else None
        if param_type is None: continue

        injected_kwargs[parameter_name] = param_type
    
    old_init = cls.__init__
    new_sig = _get_updated_signature(old_init, injected_kwargs)

    @wraps(old_init)
    def new_init(self, *args, **kwargs):
        kwargs.update(_get_injected_services(injected_kwargs))
        old_init(self, *args, **kwargs)

    new_init.__signature__ = new_sig
    cls.__init__ = new_init

    return cls