from rest_framework import serializers
from reviews.serializers import PopulatedReviewSerializer
from ..models import *


# the class used to control how a Game is serialized to JSON. Derives/inherits from the default ModelSerializer
class GameSerializer(serializers.ModelSerializer):
    class Meta:

        # The class type i want to serialize
        model = Game

        # Which fields to serialize to JSON. __all__ means all fields
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:

        # The class type i want to serialize
        model = Category

        # Which fields to serialize to JSON. __all__ means all fields
        fields = ('__all__')


# the class used to control how a Developer is serialized to JSON. Derives/inherits from the default ModelSerializer
class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:

        model = Developer

        fields = ('__all__')


# the class used to control how a Genre is serialized to JSON. Derives/inherits from the default ModelSerializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:

        model = Genre

        fields = ('__all__')

# Nested serializer is derived/inherited from the GameSerializer. It has extra serializers for nested objects


class PopulatedGameSerializer(GameSerializer):

    # When a 'developer' property is found on the object, it will use this serializer
    developer = DeveloperSerializer()

    # When a 'genres' property is found on the object, it will use this serializer
    genres = GenreSerializer(many=True)

    reviews = PopulatedReviewSerializer(many=True)

    categories = CategorySerializer(many=True)


class GameWithGenresSerializer(GameSerializer):

    genres = GenreSerializer(many=True)


class PopulatedDeveloperSerializer(DeveloperSerializer):

    games = GameWithGenresSerializer(many=True)
