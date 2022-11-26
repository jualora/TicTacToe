from django.urls import path
from tttApp.api import UserAPI, GameAPI

urlpatterns = [
    path('api/user/', UserAPI.as_view()),
    path('api/user/<int:idUser>/', UserAPI.as_view()),
    path('api/user/put_delete/<int:idUser>/', UserAPI.as_view()),
    path('api/user/login/', UserAPI.as_view()),
    path('api/game/', GameAPI.as_view()),
    path('api/game/<int:idGame>/', GameAPI.as_view()),
    path('api/game/<int:idGame>/user/', GameAPI.as_view()),
    path('api/game/<int:idGame>/move/', GameAPI.as_view()),
]