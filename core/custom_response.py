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
