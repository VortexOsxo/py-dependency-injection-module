from ..config import _RegisterConfig
from ..factories import SingletonFactory, TransientFactory

def _get_factory_from_config(register_config: _RegisterConfig):
    if register_config.is_singleton:
        return SingletonFactory(register_config)
    return TransientFactory(register_config)