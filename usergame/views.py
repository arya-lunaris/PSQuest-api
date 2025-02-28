from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import UserGame, Game
from .serializers.common import UserGameSerializer
from rest_framework import status
from django.utils import timezone


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
 
    
class SaveGameView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user  

        try:
            title = data.get("title", None)
            if not title:
                return Response({"message": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

            cover_url = data.get("cover", "https://via.placeholder.com/150") 
            first_release_date = data.get("first_release_date") or timezone.now().date()  
            total_rating = data.get("total_rating", None)
            genres = data.get("genres", [])
            storyline = data.get("storyline", "Storyline unavailable")
            
            game_status = data.get("status", "wishlist")  

            game, created = Game.objects.get_or_create(
                title=title,
                defaults={  
                    "cover": cover_url,
                    "first_release_date": first_release_date,
                    "total_rating": total_rating,
                    "genres": genres,
                    "storyline": storyline
                }
            )

            user_game, user_game_created = UserGame.objects.get_or_create(
                user=user, 
                game=game,
                defaults={"game_status": game_status}  
            )

            if user_game_created:
                return Response({
                    "message": f"Game added to your {game_status}!",
                    "game_id": game.id
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": f"Game is already in your {game_status}." 
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)


class UserGameByStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, status_type):
        if status_type not in ["wishlist", "collection"]:
            return Response({"message": "Invalid status type."}, status=status.HTTP_400_BAD_REQUEST)

        user_games = UserGame.objects.filter(user=request.user, status=status_type)
        serialized_games = UserGameSerializer(user_games, many=True)
        return Response(serialized_games.data)
