from django.contrib import admin
from .models import Survey, Response

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'image']}),
        ('Music Files', {'fields': ['music_file_1', 'music_file_2']}),
    ]
    inlines = [ResponseInline]

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'preferred_music')
    list_filter = ['survey']
    search_fields = ['survey__title', 'preferred_music']

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
