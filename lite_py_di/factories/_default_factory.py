from typing import Type, TypeVar
from .._init_utils import _get_init_arguments
from ..config import _RegisterConfig
from .abstract_factory import AbstractFactory

ServiceType = TypeVar('ServiceType')

class _DefaultFactory(AbstractFactory[ServiceType]):
    @property
    def class_type(self) -> Type[ServiceType]:
        return self.register_config.class_type

    def __init__(self, register_config: _RegisterConfig):
        self.register_config = register_config

    def default_create_service(self, container) -> ServiceType:
        constructor_args = _get_init_arguments(self.class_type)
        args = [container.get(arg) for arg in constructor_args]
        return self.class_type(*args)
