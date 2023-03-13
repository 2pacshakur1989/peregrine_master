class AccessDeniedError(Exception):
    def __init__(self, message="Access denied. Check if dals are accessible for this Facade."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"
    

class UserNotFoundError(Exception):
    def __init__(self, message="User not found."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"
    

class CannotRemoveFlight(Exception):
    def __init__(self, message="This flight has purchased tickets thus cannot be removed"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"
    

class CannotRemoveAirline(Exception):
    def __init__(self, message="This airline has on going flights thus cannot be removed"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"
    

class CannotRemoveCustomer(Exception):
    def __init__(self, message="This customer has on going active ticket/s thus cannot be removed"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"
    

