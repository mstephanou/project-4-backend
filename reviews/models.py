from django.db import models
from django.contrib.auth import get_user_model
from games.models import Game
User = get_user_model()

class Review(models.Model):

    text = models.TextField(max_length=300)
    owner = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name="reviews", on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.game} written by: {self.owner} on: {self.created_date}"


