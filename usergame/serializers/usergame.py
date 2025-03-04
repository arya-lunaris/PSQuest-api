from rest_framework import serializers
from usergame.models import UserGame
from game.models import Game
from game.serializers.common import GameSerializer 

class FullUserGameSerializer(serializers.ModelSerializer):
    PAGE_STATUS_CHOICES = [
        ('collection', 'Collection'),
        ('wishlist', 'Wishlist'),
    ]
    
    GAME_STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('currently_playing', 'Currently Playing'),
        ('completed', 'Completed'),
    ]
    
    page_status = serializers.ChoiceField(choices=PAGE_STATUS_CHOICES)
    
    game_status = serializers.ChoiceField(choices=GAME_STATUS_CHOICES)
    
    game = GameSerializer()

    class Meta:
        model = UserGame
        fields = ['id', 'user', 'game', 'page_status', 'game_status', 'rating', 'review']
