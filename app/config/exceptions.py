from rest_framework.views import exception_handler

def core_exception_handler(exc, context):
    """
    Overloading the standard exception handler.
    """

    # If an exception occurs that does not need to be handled manually, it will be handled by the default way."
    response = exception_handler(exc, context)

    # If response is None, it means that exception is not handled by the default handler,
    # hence we return None and let DRF handle it further.
    if response is None:
        return None

    # Handling all exceptions by wrapping the response data in an "errors" key
    return _handle_generic_error(exc, context, response)

def _handle_generic_error(exc, context, response):
    """
    Append the "errors" key to the response
    """
    response.data = {
        "errors": response.data
    }

    return response
