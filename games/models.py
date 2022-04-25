from django.db import models

# Create your models here.


# Define a Developer model, Django will se the db up for me
class Developer(models.Model):
  # Text field with a maximum length, validation is automatically handled
    title = models.CharField(max_length=100)

    # Function that defines how i want the Developer model to look in the admin area of Django, when converting the object into a string.
    def __str__(self):
        return self.title


class Genre(models.Model):
    # Text field with a maximum length, validation is automatically handled
    title = models.CharField(max_length=30)

    # Function that defines how i want the Genre model to look in the admin area of Django, when converting the object into a string.
    def __str__(self):
        return self.title


class Category(models.Model):
    # Text field with a maximum length, validation is automatically handled
    name = models.CharField(max_length=30)

    # Function that defines how i want the Genre model to look in the admin area of Django, when converting the object into a string.
    def __str__(self):
        return self.name


# Define a Game model, Django will se the db up for me
class Game(models.Model):
  # Text field with a maximum length, validation is automatically handled
    title = models.CharField(max_length=50)
  # One to many relationship with Developer (Developer had many games, but a Game can only be made by one developer)
  # on_delete models.CASCADE - when a developer is deleted, all games related to that developer is also deleted.
  # Creates a foreign key column in my 'games_game' table referencing developer_id
    developer = models.ForeignKey(
        Developer, related_name='games', on_delete=models.CASCADE, null=True)

    # text field with maximum length
    # blank=true allows empty values to be set here
    image = models.CharField(max_length=200, blank=True)

    # DateField that allows nulls
    release_date = models.DateField(null=True)

    platform = models.CharField(max_length=50, blank=True)

    # Many-to-many relationship (A game can belong to many genres, a genre can apply to many games)
    # related_name value allows me to customise what the relationship looks like from the Genre perspective (i.e. a genre has 'games')
    # blank=True allows empty values to be set (a game doesn't need to have a genre)
    genres = models.ManyToManyField(Genre, related_name='games', blank=True)

    categories = models.ManyToManyField(
        Category, related_name='games', blank=True)
