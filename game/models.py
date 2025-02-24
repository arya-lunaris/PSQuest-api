from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=200)
    cover = models.URLField()  
    first_release_date = models.DateField()
    total_rating = models.FloatField()
    genres = models.JSONField()  
    age_ratings = models.JSONField()  
    storyline = models.TextField()  

    def __str__(self):
        return self.title