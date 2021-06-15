from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('index', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('anime/edit/<int:id>', views.edit_page),
    path('anime/<int:id>', views.view_anime),
    path('login', views.login),
    path('logout', views.logout),
    path('anime/new', views.create_page),
    path('create_new', views.create_new),
    path('edit_anime/<int:id>', views.edit_anime),
    path('delete/<int:id>', views.delete_anime),
    path('editProfile/<int:id>', views.editProfile),
    path('editForm/<int:id>', views.editForm),
]
