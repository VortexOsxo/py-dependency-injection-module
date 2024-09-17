from ..errors import UnregisteredService, ServiceNotFound
from .._init_utils import _get_init_arguments
from .._singleton import SingletonMeta
from ._registry import _Registry
from ..config import ServiceConfig, _RegisterConfig
from typing import Dict, Type, TypeVar

ServiceType = TypeVar('ServiceType')

class Container(metaclass = SingletonMeta):
    """A container for managing service registration and retrieval."""
    _registry = _Registry()
    _instances: Dict[str, object] = {}

    @classmethod
    def register(cls, class_type: Type, service_config: ServiceConfig):
        """Register a service with the Container.

        Args:
            class_type (type): The type of the service class.
            service_config (ServiceConfig): Configuration for the service.
        """
        register_config = _RegisterConfig(service_config.is_singleton, class_type)
        cls._registry.register(register_config)

    @classmethod
    def get(cls, class_type: Type[ServiceType]) -> ServiceType:
        """Get an instance of a registered service.
        Args:
            class_type (type): The type of the service class.
        Returns:
            ServiceType: An instance of the service class.
        """
        return cls._get_service_intern(class_type)

    @classmethod
    def get_by_name(cls, class_name: str) -> ServiceType:
        """Get an instance of a registered service by its class name.
        Args:
            class_name (str): The name of the service class.
        Returns:
            ServiceType: An instance of the service class.
        """
        if not cls._registry.is_registered(class_name): raise ServiceNotFound(class_name)

        class_type = cls._registry.get_class_type(class_name)
        return cls._get_service_intern(class_type)

    @classmethod
    def _get_service_intern(cls, class_type: Type[ServiceType]) -> ServiceType:
        if not cls._registry.is_registered(class_type.__name__): raise UnregisteredService(class_type)
        
        if cls._registry._is_singleton(class_type):
            return cls._instances[class_type] if class_type in cls._instances else cls._create_and_save_service(class_type)
        return cls._create_service(class_type)

    @classmethod
    def _create_and_save_service(cls, class_type: Type[ServiceType]) -> ServiceType:
        service = cls._create_service(class_type)
        cls._instances[class_type] = service
        return service

    @classmethod
    def _create_service(cls, class_type: Type[ServiceType]) -> ServiceType:
        constructor_args = _get_init_arguments(class_type)
        args = [cls.get(arg) for arg in constructor_args]
        return class_type(*args)
