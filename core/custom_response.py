from rest_framework.response import Response
from rest_framework import status

class CustomResponse(Response):
    """
    A custom response class for Django REST Framework
    """
    def __init__(self, data=None, status_code=status.HTTP_200_OK, **kwargs):
        if status_code==status.HTTP_500_INTERNAL_SERVER_ERROR:
            response = {
                "error": {
                    "message": "An unexpected error occurred.",
                    "description": str(data) if isinstance(data, Exception) else data
                }
            }

        if status_code==status.HTTP_400_BAD_REQUEST:
            response = {
                "error": {
                    "message": "Validation failed.",
                    "description": "Please check the input data.",
                    "fields": data if isinstance(data, dict) else None
                }
            }
        else:
            response = {
                "data": data
            }
        super().__init__(response, **kwargs)