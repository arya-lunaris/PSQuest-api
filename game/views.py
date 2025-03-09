from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Game
from .serializers.common import GameSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from utils.igdb_api import IGDBAPI, GENRE_MAPPING
from datetime import datetime


class GameListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        game = Game.objects.all()
        game_serialized = GameSerializer(game, many=True)
        return Response(game_serialized.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)
        
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 402)


class GameDetailView(APIView):
    permission_classes = [IsAuthenticated]

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
        
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)
        
        serializer = GameSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 402)

    def delete(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise NotFound(detail="Game not found.")
        
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)
        
        game.delete()
        return Response(status=204)


class FetchIGDBGames(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_term = request.query_params.get('search', None)

        if not search_term:
            return Response({"detail": "Search term is required."}, status=400)

        igdb_api = IGDBAPI()
        try:
            games = igdb_api.search_games(
                search_term, 
                fields="id,name,cover.url,first_release_date,total_rating,genres,storyline", 
                limit=500
            )

            fixed_games = []
            for game in games:
                if isinstance(game, dict):

                    game['title'] = game.pop('name', None)

                    if game.get('cover') and game['cover'].get('url'):
                        cover_url = game['cover']['url']
                        
                        if cover_url.startswith('//'):
                            cover_url = 'https:' + cover_url

                        if 't_thumb' in cover_url:
                            cover_url = cover_url.replace("t_thumb", "t_cover_big") 

                        game['cover'] = cover_url
                    else:
                        game['cover'] = None  

                    game['genres'] = [GENRE_MAPPING.get(genre, f"Unknown Genre ({genre})") for genre in game.get('genres', [])]

                    if isinstance(game.get('first_release_date'), int):
                        game['first_release_date'] = datetime.utcfromtimestamp(game['first_release_date']).strftime('%Y-%m-%d')

                    if isinstance(game.get('total_rating'), (float, int)):
                        game['total_rating'] = round(game['total_rating'])

                    fixed_games.append(game)

            serializer = GameSerializer(data=fixed_games, many=True)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response({"detail": "Invalid game data.", "errors": serializer.errors}, status=400)

        except Exception as e:
            return Response({"detail": str(e)}, status=400)
