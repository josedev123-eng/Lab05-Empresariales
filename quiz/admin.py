from django.contrib import admin
from .models import Exam, Question, Choice


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date")
    search_fields = ("title",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "exam")


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct")
    list_filter = ("is_correct",)