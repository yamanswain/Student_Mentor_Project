from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Student._meta.fields]


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mentor._meta.fields]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Question._meta.fields]
