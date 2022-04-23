from django.shortcuts import render
# status gives me a list of possible response codes
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
# This imports rest_frameworks APIView that i will use to extend my custom view
from rest_framework.views import APIView
# Response creates a way to send a HTTP resppnse to the user making the request, passing back data and other info
from rest_framework.response import Response
# Import NotFound when adding error handling, provides a default response when data is Not Found
from rest_framework.exceptions import NotFound
# import all my models as i'm using them in these views
from .models import *
# import all my serializers as i'm using them in these views
from .serializers.common import *
# Create your views here.

# GENERIC GAME VIEWS AUTOMATES MOST OF THE API ENDPOINT FUNCTIONAILITY FOR ME

# List Games generic view


class GameList(ListCreateAPIView):

    # This will query will handle all games
    queryset = Game.objects.all()

    # Chooses which serializer to use
    serializer_class = PopulatedGameSerializer


# Update or Destroy Games generic view
class GameUpdateDestroy(RetrieveUpdateDestroyAPIView):

    # Handles all games
    queryset = Game.objects.all()

    # Chooses which serializer to use
    serializer_class = GameSerializer


# Get Game by ID generic view
class GameDetail(RetrieveAPIView):

    # Handles all books
    queryset = Game.objects.all()

    # Chooses serializer
    serializer_class = PopulatedGameSerializer


# Developer class-based views
# More basic, fine-grain control of the API endpoint

class DeveloperListCreate(APIView):
    # List Developers
    def get(self, request):
        # Load all developers from the database
        developers = Developer.objects.all()

    # Serialize the developers to JSON by using a DeveloperSerializer with the many=true flag
        serialized_developers = PopulatedDeveloperSerializer(
            developers, many=True)
    # Return the serialized developers with a HTTP 200
        return Response(data=serialized_developers.data, status=status.HTTP_200_OK)

    # Create Developer

    def post(self, request):
        # Create a new serializer with the incoming new developer request data
        developer_serializer = DeveloperSerializer(data=request.data)

        # Check whether the new developer is valid
        if developer_serializer.is_valid():

            # New developer is valid so save it to the database
            developer_serializer.save()

            # Saved data returns 200 response and the new developer record
            return Response(data=developer_serializer.data, status=status.HTTP_200_OK)

        # Incoming update is not valid so return a http 400 bad request
        return Response(data=developer_serializer.data, status=status.HTTP_400_BAD_REQUEST)


# Developer retrieve, update and delete class-based view
class DeveloperRetrieveUpdateDelete(APIView):

    # Get developer by ID - pk is the primary key, passed through our <int:pk> route in urls.py
    def get(self, request, pk):
        # Call the get_developer function which will either get the author or raise a HTTP 404 status code response if not present
        developer = self.get_developer(pk=pk)

        # Create a new serializer with the current developer data - we're only returning one author so we don't need the many=True flag
        serialized_developer = DeveloperSerializer(developer)

        # Return the serialized developer data and a HTTP 200 response
        return Response(data=serialized_developer.data, status=status.HTTP_200_OK)


# Update Developer by ID - pk is the primary key, passed through our <int:pk> route in urls.py

    def put(self, request, pk):

        # Call the get_developer function which will either get the author or raise a HTTP 404 status code response if not present
        developer_to_update = self.get_developer(pk=pk)

        # Create a new serializer with the current developer data and apply the changes from the incoming request data (updated developer)
        # We specify the key `data` because we aren't adhering to the order of the arguments, same as `pk=pk` and `many=True`
        updated_developer = DeveloperSerializer(
            developer_to_update, data=request.data)

        # Check whether the updates are valid
        if updated_developer.is_valid():

            # Updates are valid so save them to the database
            updated_developer.save()

            # Data has been saved return a 200 response and the updated data
            return Response(updated_developer.data, status=status.HTTP_200_OK)

        # Incoming update is not valid so return a HTTP 400 bad request response
        return Response(data=updated_developer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Developer by ID - pk is the primary key, passed through our <int:pk> route in urls.py

    def delete(self, request, pk):

        # Call the get_developer function which will either get the developer or raise a HTTP 404 status code response if not present
        developer_to_delete = self.get_developer(pk=pk)

        # Delete the develper record
        developer_to_delete.delete()

        # Return a successful HTTP 204 response
        return Response(status=status.HTTP_204_NO_CONTENT)

    # This is an internal function that doesn't directly handle incoming requests. It is called by other functions in this class. This avoids repeating the same code in each function to handle a missing developer.

    def get_developer(self, pk):

        # Use a `try` here so if the code within it throws an exception it will be caught in the `except` block and handled rather than returning a HTTP 500 server error response code
        try:
            # Get the author from the database if it exists. If not, an Author.DoesNotExist error will be raised
            return Developer.objects.get(pk=pk)

        # Django Models have a DoesNotExist exception that occurs when a query returns no results
        # Link: https://docs.djangoproject.com/en/4.0/ref/models/class/#model-class-reference
        # Developer.DoesNotExist errors are caught and handled here
        except Developer.DoesNotExist:

            # Raising a NotFound error will return a HTTP 404 response on the API. Further execution of the code will cease.
            # We'll also pass a custom message on the detail key so the user knows what's wrong
            # NotFound returns a 404 response
            # Link: https://www.django-rest-framework.org/api-guide/exceptions/#notfound
            # Raise and return can both be used inside an exception, but NotFound has to be raised
            # Raising an exception is when you're indicating a specific behaviour or outcome like NotFound
            # Returning an exception is for something generic like Response above
            raise NotFound(detail="Can't find that developer")


class GameSearch(APIView):

    def get(self, request):

        # Get search value from querystring, i.e. http://mydomain.com/search?book_title=The Stand
        game_title_search = request.GET.get("game_title")

        # Query the database with a filter using {fieldname}__icontains which does a case-insensitive search
        games = Game.objects.filter(title__icontains=game_title_search)

        serialized_games = PopulatedGameSerializer(games, many=True)

        return Response(data=serialized_games.data, status=status.HTTP_200_OK)
