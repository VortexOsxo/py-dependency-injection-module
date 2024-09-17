from typing import Type
from .abstract_factory import AbstractFactory, ServiceType

class SingletonFactory(AbstractFactory[ServiceType]):
    def __init__(self, class_type: Type[ServiceType]):
        self.class_type = class_type
        self.instance = None

    def get_service(self, container) -> ServiceType:
        if self.instance is None:
            self.instance = self.default_create_service(container)
        return self.instance
