
from rest_framework.response import Response
from rest_framework import status

def json_response(data=None,message:str=None,errors=None,status_code=status.HTTP_200_OK,paginate=False)->Response:
    response_data = {}
    if message is not None:
        response_data['message'] = message
    if data is not None:
        if paginate:
            response_data['data']=data.get('results')
            response_data['totalCount']=data.get('totalCount')
            response_data['groupCount']=data.get('groupCount')
        else:
            response_data['data'] = data
    if errors is not None:
        response_data['errors'] = errors

    return Response(response_data, status=status_code)
