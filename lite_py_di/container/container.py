from ..errors import UnregisteredService, ServiceNotFound
from ..utils import get_constructor_arguments
from ..singleton import SingletonMeta
from .registry import Registry
from typing import Dict, Type, TypeVar

ServiceType = TypeVar('ServiceType')

class Container(metaclass = SingletonMeta):
    """A container for managing service registration and retrieval."""
    def __init__(self):
        self.registry = Registry()
        self._instances: Dict[str, object] = {}

    def register(self, class_type: Type, is_singleton: bool):
        """Register a service with the Container.
        Args:
            class_type (type): The type of the service class.
            is_singleton (bool): Indicates if the service is a singleton.
        """
        self.registry.register(class_type, is_singleton)

    def get(self, class_type: Type[ServiceType]) -> ServiceType:
        """Get an instance of a registered service.
        Args:
            class_type (type): The type of the service class.
        Returns:
            ServiceType: An instance of the service class.
        """
        if not self.registry.is_registered(class_type.__name__): raise UnregisteredService(class_type)
        return self._get_service_intern(class_type)

    def get_by_name(self, class_name: str) -> object:
        """Get an instance of a registered service by its class name.
        Args:
            class_name (str): The name of the service class.
        Returns:
            object: An instance of the service class.
        """
        if not self.registry.is_registered(class_name): raise ServiceNotFound(class_name)

        class_type = self.registry.get_class_type(class_name)
        return self._get_service_intern(class_type)

    def _get_service_intern(self, class_type: Type[ServiceType]) -> ServiceType:
        if self.registry._is_singleton(class_type):
            return self._instances[class_type] if class_type in self._instances else self._create_and_save_service(class_type)
        return self._create_service(class_type)

    def _create_and_save_service(self, class_type: Type[ServiceType]) -> ServiceType:
        service = self._create_service(class_type)
        self._instances[class_type] = service
        return service

    def _create_service(self, class_type: Type[ServiceType]) -> ServiceType:
        constructor_args = get_constructor_arguments(class_type)
        args = [self.get(arg) for arg in constructor_args]
        return class_type(*args)
