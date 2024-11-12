from .abstract_factory import AbstractFactory, ServiceType
from typing import Type

class _TemporaryFactory(AbstractFactory):
    def __init__(self, instance: ServiceType, class_type:Type[ServiceType], old_factory: AbstractFactory = None):
        self.instance = instance
        self.class_type = class_type
        self.old_factory = old_factory
    
    def get_service(self, container):
        return self.instance
    
    def after_get(self, container):
        container.replace_factory(self.class_type, self.old_factory)