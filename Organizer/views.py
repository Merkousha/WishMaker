from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import Goal, GoalDuration, GoalType
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


@login_required
def goal_list(request):
    goals = Goal.objects.filter(parent=None,user=request.user)
    next_step_id = 1
    request.session['parent_goal_id']=None
    for goal in goals:
        goal.num_child_goals = get_goal_child_count(goal)
        goal.num_completed_child_goals = get_success_goal_child_count(goal)
        if(goal.num_child_goals==0 or goal.num_completed_child_goals == 0):
            goal.progress = 0
        else:
             goal.progress = (goal.num_completed_child_goals / goal.num_child_goals) * 100

    return render(request, 'goals/goal_list.html', {'goals': goals, 'next_step_id': next_step_id})

def get_goal_child_count(goal):
    children = Goal.objects.filter(parent=goal)
    children_count = children.count()
    for child in children:
       children_count = children_count + get_goal_child_count(child)
    return children_count

def get_success_goal_child_count(goal):
    children = Goal.objects.filter(parent=goal)
    children_count = children.filter(is_complete=1).count()
    for child in children:
       children_count = children_count + get_success_goal_child_count(child)
    return children_count


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
    children =[]
    for gl in goal.children.all() :    
        chl = gl
        chl.num_child_goals = get_goal_child_count(gl)
        chl.num_completed_child_goals = get_success_goal_child_count(gl)
        if(gl.num_child_goals==0 or gl.num_completed_child_goals == 0):
           chl.progress = 0
        else:
            chl.progress = (gl.num_completed_child_goals / gl.num_child_goals) * 100
        children.append(chl)
    return render(request, 'goals/goal_detail.html', {'goal': goal,'next_step_id':next_step_id,'children':children})


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

@login_required
def update_goal_status(request):
    if request.method == 'POST':
      try:
        goal_id = request.POST.get('goal_id')
        is_complete = request.POST.get('is_complete')
        goal = Goal.objects.get(pk=goal_id)
        goal.is_complete = bool(is_complete.lower() == "true")
        goal.save()
        return JsonResponse({'message': 'Goal status updated successfully'})
      except ObjectDoesNotExist:
            return JsonResponse({'error': 'Goal not found'}, status=404)
      except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'})