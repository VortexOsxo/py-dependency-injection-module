from typing import Type
from ._abstract_factory import _AbstractFactory, ServiceType
from ..config import _RegisterConfig
from ..errors import InvalidServiceConfiguration

class TransientFactory(_AbstractFactory[ServiceType]):
    def __init__(self, register_config: _RegisterConfig):
        super().__init__(register_config)

    def on_registration(self, container):
        if self.register_config.is_loaded_eagerly:
            raise InvalidServiceConfiguration("Service can't be transient and eagerly loaded at the same time")

    def get_service(self, container) -> ServiceType:
        return self.default_create_service(container)