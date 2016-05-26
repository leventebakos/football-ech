from django.contrib import admin
from .models import Match
from .models import Tip

def delete_tips(modeladmin, request, queryset):
    for match in queryset:
        tips = Tip.objects.filter(match = match)
        for tip in tips:
            tip.score = 0
            tip.scoring_field = ""
            tip.is_score_calculated = False
delete_tips.delete_tips = "Delete calculated scores for tips for these matches"
            
class MatchAdmin(admin.ModelAdmin):
    actions = [delete_tips]

admin.site.register(Match, MatchAdmin)
admin.site.register(Tip)
