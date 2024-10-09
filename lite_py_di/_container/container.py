from ..errors import UnregisteredService, InvalidLookUpValue, ServiceAlreadyRegistered
from .._singleton import SingletonMeta
from ..config import ServiceConfig, _RegisterConfig
from typing import Dict, Type, TypeVar
from ..factories import _AbstractFactory, _get_factory_from_config

ServiceType = TypeVar('ServiceType')

class Container(metaclass = SingletonMeta):
    """A container for managing service registration and retrieval."""
    _factories: Dict[str, _AbstractFactory] = {}

    @classmethod
    def register(cls, class_type: Type[ServiceType], service_config: ServiceConfig):
        """Register a service with the Container.
        Args:
            class_type (type): The type of the service class.
            service_config (ServiceConfig): Configuration for the service.
        """
        if class_type.__name__ in cls._factories:
            raise ServiceAlreadyRegistered(class_type)

        register_config = _RegisterConfig(service_config.is_singleton, service_config.is_loaded_eagerly, class_type)
        factory = _get_factory_from_config(register_config)

        cls._factories[class_type.__name__] = factory
        factory.on_registration(cls)

    @classmethod
    def get(cls, lookup_value: Type[ServiceType] | str) -> ServiceType:
        """Get an instance of a registered service.
        Args:
            lookup_value (type | str): The type or the name of the service class.
        Returns:
            ServiceType: An instance of the service class.
        """
        if not isinstance(lookup_value, (type, str)):
            raise InvalidLookUpValue("the service class name or type", type(lookup_value))
        class_name = lookup_value.__name__ if isinstance(lookup_value, type) else lookup_value
        return Container._get_service_intern(class_name)
    
    @classmethod
    def reset(cls) -> None:
        """ Clear all the services and instances registered in the Container
        Usage:
            Container.reset()
        """
        cls._factories = {}

    @classmethod
    def _get_service_intern(cls, class_name: str) -> ServiceType:
        if class_name not in cls._factories: raise UnregisteredService(class_name)        
        return cls._factories[class_name].get_service(cls)
