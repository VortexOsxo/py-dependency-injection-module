from typing import Type
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from .._init_utils import _get_init_arguments
from ..config import _RegisterConfig

ServiceType = TypeVar('ServiceType')

class _AbstractFactory(ABC, Generic[ServiceType]):
    @property
    def class_type(self) -> Type[ServiceType]:
        return self.register_config.class_type

    def __init__(self, register_config: _RegisterConfig):
        self.register_config = register_config

    def on_registration(self, container):        
        pass

    @abstractmethod
    def get_service(self, container) -> ServiceType:
        pass

    def default_create_service(self, container) -> ServiceType:
        constructor_args = _get_init_arguments(self.class_type)
        args = [container.get(arg) for arg in constructor_args]
        return self.class_type(*args)
