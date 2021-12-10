from django.urls import path
from . import views

urlpatterns = [
    path('', views.profilePage, name='profile-page'),
    path('user/add', views.create_user, name='create_user'),
    path('user/edit/<int:pk>', views.edit_user, name='edit_user'),
    path('user/delete/<int:pk>', views.delete_user, name='delete_user'),
]
