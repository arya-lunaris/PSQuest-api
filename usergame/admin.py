from django.contrib import admin
from usergame.models import UserGame
from game.models import Game
from django.utils.safestring import mark_safe

class UserGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_title', 'status', 'rating', 'review', 'added_on', 'game_release_date', 'game_rating', 'game_genres')

    readonly_fields = ('game_title', 'game_description', 'game_cover', 'game_release_date', 'game_rating', 'game_genres', 'status', 'rating', 'review', 'added_on')

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
        return ', '.join(obj.game.genres) 
    game_genres.short_description = 'Genres'

    fields = ('user', 'game', 'game_title', 'game_description', 'game_cover', 'game_release_date', 'game_rating', 'game_genres', 'status', 'rating', 'review', 'added_on')

admin.site.register(UserGame, UserGameAdmin)
