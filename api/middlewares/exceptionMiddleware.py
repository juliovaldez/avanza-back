from typing import Any
from rest_framework.request import Request
from rest_framework.serializers import ValidationError
from rest_framework import status
import logging
from api.utils.utils  import json_response


logger = logging.getLogger(__name__)

class ExceptionMiddleware:
    def __init__(self,get_response) -> None:
        self.get_response=get_response
    
    def __call__(self, request:Request) -> Any:
        try:
            response = self.get_response(request)
        except ValidationError as e:
            response= json_response('The given data was invalid',[],e.message_dict,status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            logger.exception(e)
            raise e
        finally:
            if response is None:
                logger.error('Excepción no manejada: %s', e, exc_info=True)
        return response