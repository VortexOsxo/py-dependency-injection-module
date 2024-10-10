from typing import TypeVar, Generic
from abc import ABC, abstractmethod

ServiceType = TypeVar('ServiceType')

class AbstractFactory(ABC, Generic[ServiceType]):
    def on_registration(self, container):        
        pass

    @abstractmethod
    def get_service(self, container) -> ServiceType:
        pass
