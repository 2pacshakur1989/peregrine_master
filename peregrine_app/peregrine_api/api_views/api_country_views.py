from rest_framework.decorators import api_view
from rest_framework.response import Response
from peregrine_app.facades.anonymousfacade import AnonymousFacade
from peregrine_app.peregrine_api.api_serializers.country_serializer import CountrySerializer
from peregrine_app.loggers import country_logger

anonymousfacade = AnonymousFacade()


@api_view(['GET'])
def country(request):

    # GET REQUESTS
    if request.method == 'GET':

        if 'id' in request.query_params:
            # Handle 'get_flights_by_origin_country' for all users
            id = request.query_params['id']
            country = anonymousfacade.get_country_by_id(request=request, country_id=id)
            serializer = CountrySerializer(country)
            country_logger.info('Get country by id attempt')
            return Response(serializer.data)
        
        else:

            countries = anonymousfacade.get_all_countries(request=request)
            serializer = CountrySerializer(countries, many=True)
            country_logger.info('Get all countries attempt')
            return Response(serializer.data)