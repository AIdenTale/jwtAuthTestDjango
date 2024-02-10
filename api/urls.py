from django.urls import path

from . import views

urlpatterns = [
    path('get_token', views.get_token_view),
    path('refresh', views.refresh_tokens_view),
    path('secret', views.secret_view)
]