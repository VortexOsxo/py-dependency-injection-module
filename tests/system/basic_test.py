import pytest
from lite_py_di import Container, service, accessor
from lite_py_di.errors import UnregisteredService, ServiceAlreadyRegistered, InvalidLookUpValue
from lite_py_di.factories import _InstanceFactory

@pytest.fixture(autouse=True)
def reset_container():
    Container.reset()
    yield

def test_basic_registration():
    @service()
    class ServiceA:
        pass

    sa = Container.get(ServiceA)

    assert isinstance(sa, ServiceA), "Container did not return the expected type."

def test_basic_dependency_injection():
    @service()
    class Dependency:
        pass

    @service()
    class Service:
        def __init__(self, dependency: Dependency):
            self.dependency = dependency

    s = Container.get(Service)
    assert isinstance(s, Service), "Container did not return the expected type."
    assert isinstance(s.dependency, Dependency), "Container did not give the proper dependency."

def test_get_by_name():
    @service()
    class ServiceA:
        pass

    a = Container.get('ServiceA')
    assert isinstance(a, ServiceA), "Should be able to get services by name."

def test_unregistered_service():
    with pytest.raises(Exception) as error:
        Container.get('ServiceA')
    assert isinstance(error.value, UnregisteredService), "Should give proper error message when service is not found."

def test_registering_service_twice():
    with pytest.raises(Exception) as error:
        @service()
        class ServiceA:
            pass

        @service()
        class ServiceA:
            pass

    assert isinstance(error.value, ServiceAlreadyRegistered), "Should give proper error message when service is already registered."

def test_get_with_wrong_parameter():
    with pytest.raises(Exception) as error:
        Container.get(1)
    assert isinstance(error.value, InvalidLookUpValue), "Should give proper error message when getting with a wrong lookup value."

def test_register_instance():
    class Service:
        pass

    service = Service()

    Container.register_instance(Service, service)

    assert Container.get(Service) is service, "Should be able to register an instance of a service."

def test_accessor():
    @service()
    class Service:
        pass

    @accessor
    class Accessor:
        def __init__(self, service: Service):
            self.service = service

    a = Accessor()
    assert isinstance(a.service, Service), "Should be able to inject the service inside of the constructor."

def test_replace_factory():
    class Service:
        pass

    service1 = Service()
    service2 = Service()

    factory1 = _InstanceFactory(service1)
    factory2 = _InstanceFactory(service2)

    Container.register_factory(Service, factory1)
    assert Container.get(Service) is service1, "Should be able to replace even if there is no factory registered yet."

    Container.replace_factory(Service, factory2)
    assert Container.get(Service) is service2, "Should be able to replace the factory."

def test_temporary_instance():
    @service()
    class Service:
        pass

    instance1 = Container.get(Service)

    instance2 = Service()
    Container.register_temporary(Service, instance2)

    assert Container.get(Service) is instance2, "Should be able to temporarily replace a factory with an instance."
    assert Container.get(Service) is instance1, "Should be able to restore the previous factory."