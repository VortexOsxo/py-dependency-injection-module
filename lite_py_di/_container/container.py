from ..errors import UnregisteredService, ServiceNotFound
from .._singleton import SingletonMeta
from ._registry import _Registry
from ..config import ServiceConfig, _RegisterConfig
from typing import Dict, Type, TypeVar
from ..factories import _AbstractFactory

ServiceType = TypeVar('ServiceType')

class Container(metaclass = SingletonMeta):
    """A container for managing service registration and retrieval."""
    _registry = _Registry()
    _factories: Dict[Type[ServiceType], _AbstractFactory] = {}

    @classmethod
    def register(cls, class_type: Type[ServiceType], service_config: ServiceConfig):
        """Register a service with the Container.

        Args:
            class_type (type): The type of the service class.
            service_config (ServiceConfig): Configuration for the service.
        """
        register_config = _RegisterConfig(service_config.is_singleton, service_config.is_loaded_eagerly, class_type)

        factory = cls._registry.register(register_config)
        cls._factories[class_type] = factory
        factory.on_registration(cls)

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
    def reset(cls) -> None:
        """ Clear all the services and instances registered in the Container
        Usage:
            Container.reset()
        """
        cls._registry = _Registry()
        cls._factories = {}

    @classmethod
    def _get_service_intern(cls, class_type: Type[ServiceType]) -> ServiceType:
        if not cls._registry.is_registered(class_type.__name__): raise UnregisteredService(class_type)
        
        if not class_type in cls._factories: raise UnregisteredService(class_type)
        return cls._factories[class_type].get_service(cls)
