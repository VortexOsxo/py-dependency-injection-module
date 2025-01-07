from lite_py_di import Container, service, ServiceConfig
import pytest

@pytest.fixture(autouse=True)
def reset_container():
    Container.reset()
    yield

def test_default_service():
    try:
        @service
        class Service:
            def greet(self):
                return "Hello, World!"
        assert True
    
    except: assert False, 'Could not register a service with the default method'
    
def test_default_container():
    @service
    class Service:
        def greet(self):
            return "Hello, World!"

    service1 = Container.get(Service)
    service2 = Container.get('Service')

    assert service1 is service2
    assert service1 is not None
    assert isinstance(service1, Service)

def test_transient():
    @service(ServiceConfig(is_loaded_eagerly=False, is_singleton=False))
    class TransientService:
        pass

    service1 = Container.get(TransientService)
    service2 = Container.get(TransientService)
    assert service1 != service2

def test_dependency_injection():
    @service()
    class Dependency:
        pass

    @service()
    class Dependency2:
        def func(self):
            pass

    @service()
    class Service:
        def __init__(self, dependency: Dependency, dependency2: Dependency2):
            self.dependency = dependency
            dependency2.func()

    s = Container.get(Service)
    assert isinstance(s, Service), "Container did not return the expected type."
    assert isinstance(s.dependency, Dependency), "Container did not give the proper dependency."