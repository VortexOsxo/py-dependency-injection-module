import pytest
from lite_py_di import Container, service, ServiceConfig

@pytest.fixture(autouse=True)
def reset_container():
    Container.reset()
    yield

def test_singleton():
    @service()
    class ServiceA:
        pass

    sa1 = Container.get(ServiceA)
    sa2 = Container.get(ServiceA)

    assert sa1 is sa2

def test_transient():
    @service(ServiceConfig(is_singleton=False))
    class ServiceB:
        pass

    sb1 = Container.get(ServiceB)
    sb2 = Container.get(ServiceB)

    assert sb1 is not sb2 