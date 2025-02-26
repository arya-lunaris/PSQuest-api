from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=200)
    cover = models.URLField(null=True, blank=True) 
    first_release_date = models.DateField()
    total_rating = models.FloatField(null=True, blank=True)  
    genres = models.JSONField(default=list, null=True, blank=True)  
    storyline = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
