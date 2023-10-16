from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import Goal, GoalDuration, GoalType, DailyTask
from django.contrib.auth.decorators import login_required

@login_required
def goal_list(request):
    goals = Goal.objects.filter(parent=None,user=request.user)
    next_step_id = 1
    request.session['parent_goal_id']=None
    return render(request, 'goals/goal_list.html', {'goals': goals,'next_step_id':next_step_id})

@login_required
def create_goal(request,next_step_id=None):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        goal_type_id = request.POST['goal_type']  # Assuming 'goal_type' is the name of the dropdown field in your form
        duration_id = request.POST['duration']  # Assuming 'duration' is the name of the dropdown field in your form
        parent_goal_id = request.POST.get('parent_goal', None)  # Optional, if you allow linking to a parent goal
        # Access the current user from the request
        user = request.user
        goal_type = GoalType.objects.get(pk=goal_type_id)
        duration = GoalDuration.objects.get(pk=duration_id)

        # Create the new goal
        new_goal = Goal(title=title, description=description, goal_type=goal_type, duration=duration,user=user)

        print(request.user)   
        # If this is a child goal, link it to the parent goal
        if parent_goal_id:
            parent_goal = Goal.objects.get(pk=parent_goal_id)
            new_goal.parent = parent_goal

        new_goal.save()

        # Redirect to the goal list page after creating the goal
        return redirect('goal_list')
    else:
        goal_types = GoalType.objects.all()
        if next_step_id == None :
            goal_durations = GoalDuration.objects.all()
            goals = Goal.objects.all()
        else :
               parent_goal_id = request.session.get('parent_goal_id', None)
               goal_durations = GoalDuration.objects.filter(pk=next_step_id)
               next_step_id = next_step_id + 1
               if (parent_goal_id == None):
                goals = Goal.objects.filter(duration__pk=next_step_id)
               else :
                goals = Goal.objects.filter(pk=parent_goal_id)
        print (next_step_id)     
        print (parent_goal_id)               
          
        return render(request, 'goals/create_goal.html', {'goal_types': goal_types, 'goal_durations': goal_durations , 'goals':goals,'next_step_id':next_step_id})

@login_required
def goal_detail(request, goal_id):
    goal = Goal.objects.get(pk=goal_id ,user=request.user)
    next_step_id = goal.duration.pk + 1
    request.session['parent_goal_id'] = goal.pk
    return render(request, 'goals/goal_detail.html', {'goal': goal,'next_step_id':next_step_id})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('goal_list')  # Redirect to your desired page after registration
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})