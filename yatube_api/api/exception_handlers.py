from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений для API.
    """
    if isinstance(exc, (InvalidToken, TokenError)):
        return Response(
            {
                'detail': 'Token is invalid or expired',
                'code': 'token_not_valid'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    return exception_handler(exc, context)
