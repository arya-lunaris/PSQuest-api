from rest_framework.serializers import ModelSerializer
from ..models import Game

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},  
            'cover': {'required': False, 'allow_null': True},  
            'first_release_date': {'required': False, 'allow_null': True},  
            'total_rating': {'required': False, 'allow_null': True}, 
            'storyline': {'required': False, 'allow_null': True},  
            'genres': {'required': False},  
        }
