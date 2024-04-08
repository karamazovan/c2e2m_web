from django.contrib import admin
from .models import Survey, Response, Demographic, SurveyResponse

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'image']}),  # 'None' no section title
        ('Music Files', {'fields': ['music_file_1', 'music_file_2']}),  # 'Music Files' section
    ]
    inlines = [ResponseInline]  # Survey object or edit -> Response inline

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'user', 'question', 'preferred_music')
    list_filter = ('survey', 'user', 'question')
    search_fields = ('survey__title', 'user__username', 'question__text')

class DemographicAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'music_experience')
    list_filter = ('age', 'gender', 'music_experience')
    search_fields = ('user__username',)

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_mood', 'colour_association', 'music_mood_influence')
    list_filter = ('current_mood', 'music_mood_influence')
    search_fields = ('user__username', 'colour_association')

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Demographic, DemographicAdmin)
admin.site.register(SurveyResponse, SurveyResponseAdmin)