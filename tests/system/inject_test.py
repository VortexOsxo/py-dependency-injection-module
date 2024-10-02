import pytest
from lite_py_di import Container, service, inject

@pytest.fixture(autouse=True)
def reset_container():
    Container.reset()
    yield

def test_inject_with_service():
    @service()
    class Service:
        value = 10

    @inject(service=Service)
    def hello(value, service):
        assert isinstance(service, Service), "Service should be properly injected"
        return service.value + value

    result = hello(5)
    assert result == 15

def test_inject_with_default_value():
    @service()
    class Service:
        value = 1

    @inject(service=Service)
    def add1(value, second_value=0, service=None):
        assert second_value == 0, "Default value should work properly"
        assert isinstance(service, Service), "Service should be properly injected"
        return value + second_value + service.value
    
    assert add1(1) == 2, "Method using injection should work properly"

    @inject(service=Service)
    def add2(value, second_value=0, service=None):
        assert second_value == 3, "Should be able to specify the default value"
        assert isinstance(service, Service), "Service should be properly injected"
        return value + second_value + service.value
    
    assert add2(2, 3) == 6

def test_inject_with_methods():
    @service()
    class Service:
        value = 1

    class TestClass():
        def __init__(self):
            self.value = 2

        @inject(service=Service)
        def calcul(self, value, service=None):
            assert isinstance(service, Service), "Service should be properly injected"
            return self.value + value + service.value
        
    t = TestClass()
    assert t.calcul(3) == 6

def test_inject_with_service_name():
    @service()
    class Service:
        value = 10

    @inject(service='Service')
    def hello(value, service):
        assert isinstance(service, Service), "Service should be properly injected"
        return service.value + value

    result = hello(5)
    assert result == 15

def test_multiple_injections():
    @service()
    class ServiceA:
        value = 10

    @service()
    class ServiceB:
        value = 8

    @inject(serviceA=ServiceA, serviceB=ServiceB)
    def hello(value, serviceA, serviceB):
        assert isinstance(serviceA, ServiceA), "Service should be properly injected"
        assert isinstance(serviceB, ServiceB), "Second service should be properly injected"
        return serviceA.value + serviceB.value + value

    result = hello(5)
    assert result == 23
