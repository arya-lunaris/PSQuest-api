from rest_framework import serializers
from usergame.models import UserGame
from game.models import Game
from game.serializers.common import GameSerializer 

class FullUserGameSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    
    class Meta:
        model = UserGame
        fields = ['id', 'user', 'game', 'page_status', 'game_status', 'rating', 'review']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        game = instance.game

        game_data = GameSerializer(game).data
        representation['game'] = game_data 
        
        return representation
