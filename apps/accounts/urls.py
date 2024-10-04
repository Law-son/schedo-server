from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/', views.get_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # path('change-password/', views.change_password, name='change_password'),
]
