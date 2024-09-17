class UnspecifiedType(Exception):
    def __init__(self, class_type: type):
        super().__init__(f"all init arguments of {class_type.__name__} must specify their types")

class UnregisteredService(Exception):
    def __init__(self, class_type: type):
        super().__init__(f"{class_type.__name__} is not registered as a service")

class ServiceNotFound(Exception):
    def __init__(self, class_name: str):
        super().__init__(f"{class_name} was not found")

class ServiceAlreadyRegistered(Exception):
    def __init__(self, class_type: type):
                super().__init__(f"{class_type.__name__} was already registered")