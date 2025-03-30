from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('list/', views.news_list, name='list'),
    path('detail/<int:post_id>/', views.news_detail, name='detail'),
]