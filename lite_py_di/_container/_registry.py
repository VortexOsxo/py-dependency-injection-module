from ..errors import ServiceNotFound, ServiceAlreadyRegistered
from ..config import _RegisterConfig
from typing import Dict, Type, TypeVar

ServiceType = TypeVar('ServiceType')

class _Registry:
    def __init__(self):
        self._dependencies_config: Dict[str, _RegisterConfig] = {}

    def register(self, register_config: _RegisterConfig) -> None:
        class_name = register_config.class_type.__name__
        if class_name in self._dependencies_config: raise ServiceAlreadyRegistered(register_config.class_type)

        self._dependencies_config[class_name] = register_config

    def get_class_type(self, class_name) -> Type[ServiceType]:
        if not class_name in self._dependencies_config: raise ServiceNotFound(class_name)
        return self._dependencies_config[class_name].class_type

    def is_registered(self, class_name: str) -> bool:
        return class_name in self._dependencies_config

    def _is_singleton(self, class_type: Type[ServiceType]) -> bool:
        return self._dependencies_config[class_type.__name__].is_singleton