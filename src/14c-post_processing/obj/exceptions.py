class Error(Exception):
    """Base class for exceptions

    Args:
        Exception ([type]): [description]
    """
    pass

class UniqueCaseException(Error):
    """Exception raised for a unique case event.

    Attributes:
        message (str): explanation of exception.

    Methods:
        __init__ : class constructor.
    """

    def __init__(self):
        self.message = "Exception raised for unique case event"