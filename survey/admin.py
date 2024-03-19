from django.contrib import admin
from .models import Survey, Response

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 1  # 기본적으로 보여 줄 Response 입력란의 수

class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'image']}),  # 'None'은 섹션 제목 없음을 의미
        ('Music Files', {'fields': ['music_file_1', 'music_file_2']}),  # 'Music Files' 섹션
    ]
    inlines = [ResponseInline]  # Survey 객체를 보거나 수정할 때 Response 객체들을 인라인으로 표시

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'user', 'preferred_music')
    list_filter = ('survey', 'user')
    search_fields = ('survey__title', 'user__username')

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
