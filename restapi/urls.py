from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ListStock.as_view()),
    path('user-invest/', views.ListUserInvest.as_view()),
    path('user-invest-remove/', views.RemoveUserInvest.as_view()),
    path('new-port/', views.ReceiveStock.as_view()),
    path('invest-create/', views.CreateInvest.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
