from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game
from .serializers.common import GameSerializer

# Create your views here.
class GameListView(APIView):

    def get(self, request):
        game = Game.objects.all()
        game_serialized = GameSerializer(game, many=True)
        return Response(game_serialized.data)

    