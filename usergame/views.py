from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import UserGame
from .serializers.common import UserGameSerializer

# Create your views here.
class UserGameListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_games = UserGame.objects.filter(user=request.user)
        user_game_serialized = UserGameSerializer(user_games, many=True)
        return Response(user_game_serialized.data)

    def post(self, request):
        serializer = UserGameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)


class UserGameDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user_game = UserGame.objects.get(pk=pk, user=request.user)
        except UserGame.DoesNotExist:
            raise NotFound(detail="User's game not found.")
        
        user_game_serialized = UserGameSerializer(user_game)
        return Response(user_game_serialized.data)

    def put(self, request, pk):
        try:
            user_game = UserGame.objects.get(pk=pk, user=request.user)
        except UserGame.DoesNotExist:
            raise NotFound(detail="User's game not found.")
        
        serializer = UserGameSerializer(user_game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 400)

    def delete(self, request, pk):
        try:
            user_game = UserGame.objects.get(pk=pk, user=request.user)
        except UserGame.DoesNotExist:
            raise NotFound(detail="User's game not found.")
        
        user_game.delete()
        return Response(status=204)