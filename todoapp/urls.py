from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='todo-index'),
    path('update/<int:pk>/', views.update, name='todo-update'),
     path('delete/<int:pk>/', views.delete, name='todo-delete'),
     path('register/', views.register, name='register'),
     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
]

