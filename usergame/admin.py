from django.contrib import admin
from usergame.models import UserGame
from game.models import Game
from django.utils.safestring import mark_safe

class UserGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_title', 'status', 'rating', 'review', 'game_release_date', 'game_rating', 'game_genres')

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

    GENRE_MAPPING = {
    2: "Point-and-click",
    4: "Fighting",
    5: "Shooter",
    7: "Music",
    8: "Platform",
    9: "Puzzle",
    10: "Racing",
    11: "Real Time Strategy (RTS)",
    12: "Role-playing (RPG)",
    13: "Simulator",
    14: "Sport",
    15: "Strategy",
    16: "Turn-based strategy (TBS)",
    24: "Tactical",
    25: "Hack and slash/Beat 'em up",
    26: "Quiz/Trivia",
    30: "Pinball",
    31: "Adventure",
    32: "Indie",
    33: "Arcade",
    34: "Visual Novel",
    35: "Card & Board Game",
    36: "MOBA"
}


    def game_genres(self, obj):
     try:
        genres = obj.game.genres
        if isinstance(genres, str):  
            import json
            genres = json.loads(genres) 
        return ', '.join(self.GENRE_MAPPING.get(genre, f"ID:{genre}") for genre in genres)
     except Exception as e:
        return f"Error: {str(e)}"

admin.site.register(UserGame, UserGameAdmin)
