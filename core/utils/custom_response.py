from rest_framework.response import Response
from rest_framework import status


class CustomResponse(Response):
    """
    A custom response class for Django REST Framework.
    Formats responses based on status code.
    """

    def __init__(self, data=None, status_code=status.HTTP_200_OK, **kwargs):
        try:
            if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                response = {
                    "error": {
                        "message": "An unexpected error occurred.",
                        "description": str(data) if isinstance(data, Exception) else data
                    }
                }
                
            elif status_code == status.HTTP_400_BAD_REQUEST:
                response = {
                    "error": {
                        "message": "Validation failed.",
                        "description": "Please check the input data.",
                        "fields": data if isinstance(data, dict) else None
                    }
                }

            elif status_code == status.HTTP_403_FORBIDDEN:
                response = {
                    "error": {
                        "message": "Permission denied.",
                        "description": str(data) if isinstance(data, str) else "You do not have permission to perform this action."
                    }
                }

            elif status_code == status.HTTP_404_NOT_FOUND:
                response = {
                    "error": {
                        "message": "Resource not found.",
                        "description": str(data) if isinstance(data, str) else "The requested resource could not be found."
                    }
                }

            else:
                response = {
                    "data": data
                }

            super().__init__(data=response, status=status_code, **kwargs)

        except Exception as e:
            super().__init__(
                data={
                    "error": {
                        "message": "An unexpected error occurred during response formatting.",
                        "description": str(e)
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                **kwargs
            )
