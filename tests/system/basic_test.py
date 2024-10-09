import pytest
from lite_py_di import Container, service

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