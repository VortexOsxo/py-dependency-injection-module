import pytest
from lite_py_di import Container, service
from lite_py_di._container._registry import _Registry

@pytest.fixture(autouse=True)
def reset_container():
    Container._registry = _Registry()
    Container._factories = {}
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