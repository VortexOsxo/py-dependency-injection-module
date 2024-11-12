from ..errors import UnregisteredService, InvalidLookUpValue, ServiceAlreadyRegistered
from .._singleton import SingletonMeta
from ..config import ServiceConfig, _RegisterConfig
from typing import Dict, Type, TypeVar
from ..factories import AbstractFactory, _InstanceFactory, _TemporaryFactory, _get_factory_from_config

ServiceType = TypeVar('ServiceType')

class Container(metaclass = SingletonMeta):
    """A container for managing service registration and retrieval."""
    _factories: Dict[str, AbstractFactory] = {}

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
    def register_factory(cls, class_type: Type[ServiceType], factory: AbstractFactory):
        """Register a factory to create a type of service with the Container.
        Args:
            class_type (type): The type of the service class.
            factory (AbstractFactory): Factory to create the service.
        """
        if class_type.__name__ in cls._factories:
            raise ServiceAlreadyRegistered(class_type)

        cls._factories[class_type.__name__] = factory
        factory.on_registration(cls)

    @classmethod
    def replace_factory(cls, class_type: Type[ServiceType], factory: AbstractFactory):
        """Register or replace a factory to create a type of service with the Container.
        Replace the previous factory, if there was one.

        Args:
            class_type (type): The type of the service class.
            factory (AbstractFactory): Factory to create the service.
        """
        cls._factories[class_type.__name__] = factory
        factory.on_registration(cls)
    
    @classmethod
    def register_instance(cls, class_type: Type[ServiceType], instance: ServiceType):
        """Register an instance of a service to be used as a singleton.
        Args:
            class_type (type): The type of the service class.
            instance (Service): The instance of the service.
        """
        cls.register_factory(class_type, _InstanceFactory(instance))

    @classmethod
    def register_temporary(cls, class_type: Type[ServiceType], instance: ServiceType):
        """Register an instance of a service to replace a factory for one use.
        Args:
            class_type (type): The type of the service class.
            instance (Service): The instance of the service.
        """
        old_factory = cls._factories[class_type.__name__] if class_type.__name__ in cls._factories else None
        cls.replace_factory(class_type, _TemporaryFactory(instance, class_type, old_factory))

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
        service = cls._factories[class_name].get_service(cls)
        cls._factories[class_name].after_get(cls)
        return service
