from ..errors import ServiceNotFound, ServiceAlreadyRegistered
from .._service.service_config import ServiceConfig
from typing import Dict, Type, TypeVar

ServiceType = TypeVar('ServiceType')

class Registry:
    def __init__(self):
        self._dependencies_config: Dict[str, ServiceConfig] = {}

    def register(self, class_type: Type, is_singleton: bool) -> None:
        class_name = class_type.__name__
        if class_name in self._dependencies_config: raise ServiceAlreadyRegistered(class_type)

        self._dependencies_config[class_name] = ServiceConfig(class_type, is_singleton)

    def get_class_type(self, class_name) -> Type:
        if not class_name in self._dependencies_config: raise ServiceNotFound(class_name)
        return self._dependencies_config[class_name].class_type

    def is_registered(self, class_name: str) -> bool:
        return class_name in self._dependencies_config

    def _is_singleton(self, class_type: Type[ServiceType]) -> bool:
        return self._dependencies_config[class_type.__name__].is_singleton