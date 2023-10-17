from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.goal_list, name='goal_list' ),
    path('goals/', views.goal_list, name='goal_list'),
    path('update_goal_status/', views.update_goal_status, name='update_goal_status'),
    path('goals/create/<int:next_step_id>', views.create_goal, name='create_goal'),
    path('goals/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]