from . import views
from django.urls import path

urlpatterns = [
    path('signup',views.SignUpApiview.as_view(),name='signup'),
    path('login',views.LoginApiview.as_view(),name='login'),
    path('author',views.AuthorApi.as_view(),name='author'),
]