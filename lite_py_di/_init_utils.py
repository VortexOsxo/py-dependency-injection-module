from .errors import UnspecifiedType
from typing import Type
import inspect

def _has_init_method(cls: Type) -> bool:
    return hasattr(cls, '__init__') and inspect.isfunction(cls.__init__)

def _get_init_arguments(cls: Type):
    if not _has_init_method(cls): return []
    
    init_args = cls.__init__.__code__.co_varnames[1:]
    init_annotations = cls.__init__.__annotations__
    required_args = []
    for arg in init_args:
        arg_type = init_annotations.get(arg)
        if arg_type is None:
            raise UnspecifiedType(cls)
        required_args.append(arg_type)
    return required_args
