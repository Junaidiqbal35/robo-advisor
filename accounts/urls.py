from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("check_email/", views.check_email, name='check_email'),
    path("check_phone_number/", views.check_phone_number, name='check_phone_number'),
    path('login/', views.HtmxLoginView.as_view(), name='account_login'),
    path('logout/', views.logout_view, name='account_logout'),
    path('profile/', views.profile, name='profile'),  # TODO
]
