from ._default_factory import _DefaultFactory, ServiceType
from ..config import _RegisterConfig
from ..errors import InvalidServiceConfiguration

class TransientFactory(_DefaultFactory):
    def on_registration(self, container):
        if self.register_config.is_loaded_eagerly:
            raise InvalidServiceConfiguration("Service can't be transient and eagerly loaded at the same time")

    def get_service(self, container) -> ServiceType:
        return self.default_create_service(container)