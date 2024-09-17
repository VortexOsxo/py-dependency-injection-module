from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from .._init_utils import _get_init_arguments

ServiceType = TypeVar('ServiceType')

class AbstractFactory(ABC, Generic[ServiceType]):
    @abstractmethod
    def get_service(self, container) -> ServiceType:
        """Get an instance of the service, creating it if necessary following the service configuration."""
        pass

    def default_create_service(self, container) -> ServiceType:
        """Default implementation of the service creation."""
        constructor_args = _get_init_arguments(self.class_type)
        args = [container.get(arg) for arg in constructor_args]
        return self.class_type(*args)
