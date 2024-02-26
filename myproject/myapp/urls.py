from . import views
from django.urls import path

urlpatterns = [
    path('signup',views.SignUpApiview.as_view(),name='signup'),
    path('login',views.LoginApiview.as_view(),name='login'),
    path('author',views.AuthorApi.as_view(),name='author'),
    path('book',views.BookApi.as_view(),name='book'),
    path('review',views.ReviewApi.as_view(),name='review'),
    path('review-author',views.ReviewAuthor.as_view(),name='review-author'),
]