from rest_framework import serializers
from usergame.models import UserGame
from game.models import Game
from game.serializers.common import GameSerializer

class UserGameSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())

    class Meta:
        model = UserGame
        fields = '__all__'
        read_only_fields = ('user', 'game')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        game = instance.game

        game_data = GameSerializer(game).data
        representation['game'] = game_data  
        return representation
    
    def update(self, instance, validated_data):
        validated_data.pop('game', None)
        return super().update(instance, validated_data)

