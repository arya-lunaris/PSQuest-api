from rest_framework import serializers
from usergame.models import UserGame
from game.models import Game

class UserGameSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())

    class Meta:
        model = UserGame
        fields = '__all__'
        read_only_fields = ('user',)

