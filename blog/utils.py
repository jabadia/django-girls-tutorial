import warnings
from functools import wraps


def deprecated(func):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning and an exception being raised when the function is used.
    """

    @wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__, category=DeprecationWarning)
        raise DeprecationWarning("ERROR: please don't use %s" % (func.__name__,))
        return func(*args, **kwargs)

    return new_func
