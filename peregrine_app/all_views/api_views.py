from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from peregrine_app.models import Country
from peregrine_app.serializers import FlightSerializer
from django.http import JsonResponse
from peregrine_app.models import Flight
from rest_framework import status


@api_view(['GET', 'POST'])
def flight_list(request):

    if request.method == 'GET':
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        serializer = FlightSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

