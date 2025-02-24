from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Game
from .serializers.common import GameSerializer

class GameListView(APIView):

    def get(self, request):
        game = Game.objects.all()
        game_serialized = GameSerializer(game, many=True)
        return Response(game_serialized.data)


    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 402)

class GameDetailView(APIView):

    def get(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise NotFound(detail="Game not found.")
        
        game_serialized = GameSerializer(game)
        return Response(game_serialized.data)


    def put(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise NotFound(detail="Game not found.")
        
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 402)


    def delete(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise NotFound(detail="Game not found.")
        
        game.delete()
        return Response(status=204)