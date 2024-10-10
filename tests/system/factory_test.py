import pytest
from lite_py_di import Container
from lite_py_di.factories import AbstractFactory

@pytest.fixture(autouse=True)
def reset_container():
    Container.reset()
    yield

def test_register_factory():
    class Service():
        def __init__(self) -> None:
            pass

    class Factory(AbstractFactory):
        def get_service(self, container):
            return Service()

    Container.register_factory(Service, Factory())
    service = Container.get(Service)

    assert isinstance(service, Service), "Container did not return the expected type."
