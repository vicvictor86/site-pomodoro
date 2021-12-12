from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('confirm-configurations/<int:user_id>', views.confirm_configurations, name='confirm_configurations'),
    path('create-user', views.create_user, name='create_user'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('perfil', views.perfil, name='perfil'),
    path('change-information/<int:user_id>', views.change_information, name='change_information'),
]