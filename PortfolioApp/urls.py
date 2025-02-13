from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home-page'),
    path('auth/', auth_page, name='auth_page'),  # Single page for login & signup
    path('api/signup/', SignupAPIView.as_view(), name='signup_api'),
    path('api/login/', LoginAPIView.as_view(), name='login_api'),
    path('to-do/', AddTaskView.as_view(), name='to-do_api'),
    path('delete-task/<int:task_id>/', DeleteTaskView.as_view(), name='delete_task'),
]