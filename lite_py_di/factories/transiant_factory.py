from typing import Type
from .abstract_factory import AbstractFactory, ServiceType

class TransiantFactory(AbstractFactory[ServiceType]):
    def __init__(self, class_type: Type[ServiceType]):
        self.class_type = class_type

    def get_service(self, container) -> ServiceType:
        return self.default_create_service(container)