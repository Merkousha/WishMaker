from django.contrib import admin
from Organizer.models import  Goal,GoalDuration,GoalType,DailyTask

class childGoals(admin.TabularInline):
    model = Goal

class GoalModelAdmin(admin.ModelAdmin):
    inlines = [childGoals]

# Register your models here.
admin.site.register(GoalType)
admin.site.register(GoalDuration)
admin.site.register(Goal,GoalModelAdmin)
admin.site.register(DailyTask)
