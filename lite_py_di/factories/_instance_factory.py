from .abstract_factory import AbstractFactory, ServiceType

class _InstanceFactory(AbstractFactory):
    def __init__(self, instance: ServiceType):
        self.instance = instance
    
    def get_service(self, container):
        return self.instance