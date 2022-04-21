from django.shortcuts import render
from rest_framework import status # status gives us a list of possible response codes
from reviews.serializers import ReviewSerializer
from rest_framework.views import APIView # This imports rest_framework's APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a HTTP response to the user making the request, passing back data and other information
from rest_framework.permissions import IsAuthenticated

class ReviewCreate(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request):
        request.data['owner'] = request.user.id
        review_serializer = ReviewSerializer(data=request.data)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(data=review_serializer.data, status=status.HTTP_200_OK)

        # Incoming update is not valid so return a HTTP 400 bad request response
        return Response(data=review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)