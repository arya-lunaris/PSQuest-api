from django.contrib import admin
from usergame.models import UserGame
from game.models import Game
from django.utils.safestring import mark_safe
from game.genre_mapping import GENRE_MAPPING 

class UserGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_title', 'page_status', 'game_rating', 'rating', 'review', 'game_release_date', 'game_genres')

    readonly_fields = ('game_title', 'game_description', 'game_cover', 'game_release_date', 'game_rating', 'game_genres',)

    def game_title(self, obj):
        return obj.game.title
    game_title.short_description = 'Game Title'

    def game_description(self, obj):
        return obj.game.storyline  
    game_description.short_description = 'Game Description'

    def game_cover(self, obj):
        return mark_safe(f'<img src="{obj.game.cover}" width="100" />')
    game_cover.short_description = 'Game Cover'

    def game_release_date(self, obj):
        return obj.game.first_release_date
    game_release_date.short_description = 'Release Date'

    def game_rating(self, obj):
        return obj.game.total_rating
    game_rating.short_description = 'Total Rating'

    def game_genres(self, obj):
        try:
            genres = obj.game.genres  
            if not isinstance(genres, list):
                import json
                genres = json.loads(genres)  
            return ', '.join(GENRE_MAPPING.get(genre, f"{genre}") for genre in genres)
        except Exception as e:
            return f"Error: {str(e)}"

    def page_status(self, obj):
        return obj.status 
    page_status.short_description = 'Status'

admin.site.register(UserGame, UserGameAdmin)
