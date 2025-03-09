from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import UserGame, Game
from .serializers.common import UserGameSerializer
from .serializers.usergame import FullUserGameSerializer
from rest_framework import status
from datetime import datetime

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
            title = data.get("title")
            if not title:
                return Response({"message": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

            cover_url = data.get("image", "https://imgur.com/sJpWrtm.png")  
            
            first_release_date = data.get("releaseDate")
            
            if first_release_date and first_release_date != "Release Date unavailable":
                try:
                    first_release_date = datetime.strptime(first_release_date, "%Y-%m-%d").date()
                except ValueError:
                    first_release_date = None
            else:
                first_release_date = None
            
            total_rating = data.get("rating") or None  

            if isinstance(total_rating, str):
                try:
                    total_rating = float(total_rating)
                except ValueError:
                    total_rating = None

            genres = data.get("genres", [])
            if isinstance(genres, str):
                genres = [genres]  

            storyline = data.get("storyline", "Storyline unavailable")
            page_status = data.get("status", "wishlist")

            game, created = Game.objects.update_or_create(
                title=title,
                defaults={
                    "cover": cover_url if cover_url else None,
                    "first_release_date": first_release_date,
                    "total_rating": total_rating,
                    "genres": genres,
                    "storyline": storyline,
                }
            )

            user_game, created = UserGame.objects.get_or_create(user=user, game=game)
            if created:
                user_game.page_status = page_status
                user_game.save()
                return Response({
                    "message": f"Game added to your {page_status}!",
                    "game_id": game.id
                }, status=status.HTTP_201_CREATED)
            elif user_game.page_status != page_status:
                user_game.page_status = page_status
                user_game.save()
                return Response({
                    "message": f"Game moved to your {page_status}."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": f"Game is already in your {page_status}."
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class UserGameByStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, page_status_type):
        game_status = request.query_params.get("game_status", None)  

        if page_status_type not in ["wishlist", "collection"]:
            return Response({"message": "Invalid page status type."}, status=status.HTTP_400_BAD_REQUEST)

        filter_conditions = {"user": request.user, "page_status": page_status_type}

        if game_status and game_status != "all":
            if game_status not in ["not_started", "currently_playing", "completed"]:
                return Response({"message": "Invalid game status."}, status=status.HTTP_400_BAD_REQUEST)
            filter_conditions["game_status"] = game_status

        user_games = UserGame.objects.filter(**filter_conditions)
        
        serialized_games = UserGameSerializer(user_games, many=True)
        return Response(serialized_games.data)


class FullGameDetailView(APIView):
    def get(self, request, pk):
        try:
            user_game = UserGame.objects.get(pk=pk)
            serializer = FullUserGameSerializer(user_game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserGame.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)







