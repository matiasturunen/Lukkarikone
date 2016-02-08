# Custom errors

class Error(Exception):
    """ Base class for all custom exceptions in this module """
    pass

class FetchError(Error):
    """ Schelude fetch error 
    
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    
    def __init__(self, message):
        self.message = message
        