from ._default_factory import _DefaultFactory, ServiceType
from ..config import _RegisterConfig

class SingletonFactory(_DefaultFactory):
    def __init__(self, register_config: _RegisterConfig):
        super().__init__(register_config)
        self.instance = None
    
    def on_registration(self, container):
        if self.register_config.is_loaded_eagerly:
            self.instance = self.default_create_service(container)

    def get_service(self, container) -> ServiceType:
        if self.instance is None:
            self.instance = self.default_create_service(container)
        return self.instance
