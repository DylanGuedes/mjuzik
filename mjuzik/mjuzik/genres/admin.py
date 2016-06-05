from django.contrib import admin
from mjuzik.recommendations.models import Recommendation

class RecommendationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recommendation, RecommendationAdmin)

