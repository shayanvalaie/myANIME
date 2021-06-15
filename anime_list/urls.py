from django.urls import path, include

urlpatterns = [
    path('', include('anime_list_app.urls')),
]
