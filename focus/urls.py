from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name = 'index'),
    path('login/',views.log_in, name='log_in'),
    path('logout/',views.log_out,name='log_out'),
    path('<int:article_id>',views.article,name='article'),
    path('<int:article_id>/comment/',views.comment,name='comment'),
    path('<int:article_id>/favorate/',views.favorate,name='favorate'),
]
