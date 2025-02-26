from django.db import models
from django.conf import settings
from game.models import Game
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class UserGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, 
        choices=[('not_started', 'Not Started'), ('currently_playing', 'Currently Playing'), ('completed', 'Completed')],
        default='not_started'
    )
    rating = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
