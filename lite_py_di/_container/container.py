from ..errors import UnregisteredService, ServiceNotFound
from .._init_utils import _get_init_arguments
from .._singleton import SingletonMeta
from ._registry import _Registry
from ..config import ServiceConfig, _RegisterConfig
from typing import Dict, Type, TypeVar

ServiceType = TypeVar('ServiceType')

class Container(metaclass = SingletonMeta):
    """A container for managing service registration and retrieval."""
    def __init__(self):
        self._registry = _Registry()
        self._instances: Dict[str, object] = {}

    def register(self, class_type: Type, service_config: ServiceConfig):
        """Register a service with the Container.

        Args:
            class_type (type): The type of the service class.
            service_config (ServiceConfig): Configuration for the service.
        """
        register_config = _RegisterConfig(service_config.is_singleton, class_type)
        self._registry.register(register_config)

    def get(self, class_type: Type[ServiceType]) -> ServiceType:
        """Get an instance of a registered service.
        Args:
            class_type (type): The type of the service class.
        Returns:
            ServiceType: An instance of the service class.
        """
        return self._get_service_intern(class_type)

    def get_by_name(self, class_name: str) -> ServiceType:
        """Get an instance of a registered service by its class name.
        Args:
            class_name (str): The name of the service class.
        Returns:
            ServiceType: An instance of the service class.
        """
        if not self._registry.is_registered(class_name): raise ServiceNotFound(class_name)

        class_type = self._registry.get_class_type(class_name)
        return self._get_service_intern(class_type)

    def _get_service_intern(self, class_type: Type[ServiceType]) -> ServiceType:
        if not self._registry.is_registered(class_type.__name__): raise UnregisteredService(class_type)
        
        if self._registry._is_singleton(class_type):
            return self._instances[class_type] if class_type in self._instances else self._create_and_save_service(class_type)
        return self._create_service(class_type)

    def _create_and_save_service(self, class_type: Type[ServiceType]) -> ServiceType:
        service = self._create_service(class_type)
        self._instances[class_type] = service
        return service

    def _create_service(self, class_type: Type[ServiceType]) -> ServiceType:
        constructor_args = _get_init_arguments(class_type)
        args = [self.get(arg) for arg in constructor_args]
        return class_type(*args)
