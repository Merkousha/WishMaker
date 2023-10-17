from django.db import models
from django.contrib.auth.models import User

class GoalDuration(models.Model):
    title = models.CharField( max_length=90)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        app_label = "Organizer"    

class GoalType(models.Model):
    title = models.CharField( max_length=90)
    description = models.TextField()
    # value : models.models.DecimalField(max_digits=2, decimal_places=0),(_("value"))
    def __str__(self):
        return self.title
    class Meta:
        app_label = "Organizer"    
        
class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , default=1)
    duration =  models.ForeignKey(GoalDuration, on_delete=models.CASCADE,blank=False)   
    goal_type =  models.ForeignKey(GoalType, on_delete=models.CASCADE,blank=False)   
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField( max_length=90)
    description = models.TextField()
    is_complete = models.BooleanField( default=False)
    def __str__(self):
        return self.title
    
    class Meta:
        app_label = "Organizer"         
        
