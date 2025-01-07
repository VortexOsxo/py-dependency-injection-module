# Lite Py DI

## Description
Lite Py DI is a lightweight dependency injection library for Python. It helps in managing dependencies in a clean and efficient way.

## Installation
To install **Lite Py DI**, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/VortexOsxo/py-dependency-injection-module
    ```

2. Navigate to the project directory:
    ```bash
    cd py-dependency-injection-module
    ```

3. Build the package:
    ```bash
    python setup.py sdist bdist_wheel
    ```

4. Install the package into your project or virtual environment:
    ```bash
    pip install dist/lite_py_di-0.1-py3-none-any.whl
    ```
    The argument passed to `pip install` should be the path to the `.whl` file generated in the previous step.


## Usage

The main building blocks of **lite-py-di** are the services. These are object instances that can be injected into functions and methods.

Here is the simplest way to create a service:

```python
from lite_py_di import service

@service
class Service:
    def greet(self):
        return "Hello, World!"
```

Services are registered in the container, and you can access them by requesting them from the container.
You can use either the class name or the class itself as the argument.

```python
from lite_py_di import Container, service

@service
class Service:
    def greet(self):
        return "Hello, World!"

service = Container.get(Service)
service = Container.get('Service')
```

### Dependency injection
When created by the container, the service will have all its required dependencies automatically injected into its `__init__` method by the container.

```python
from lite_py_di import service

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

```

### Service Registration
You can configure your service using a service configuration object.
For example, you can define whether the service is **transient** or a **singleton**, and whether it should be **eagerly loaded** or **lazily loaded**.

```python
from lite_py_di import service, ServiceConfig

@service(ServiceConfig(is_loaded_eagerly=True, is_singleton=False))
class TransientService:
    pass
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

