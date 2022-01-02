from django.urls import path
from . import views

urlpatterns = [
    path('', views.profilePage, name='profile-page'),

    path('user/add', views.create_user, name='create_user'),
    path('user/edit/<int:pk>', views.edit_user, name='edit_user'),
    path('user/delete/<int:pk>', views.delete_user, name='delete_user'),

    path('category/add', views.create_category, name='create_category'),
    path('category/edit/<slug:slug>', views.edit_category, name='edit_category'),
    path('category/delete/<slug:slug>', views.delete_category, name='delete_category'),

    path('region/add', views.create_region, name='create_region'),
    path('region/edit/<int:pk>', views.edit_region, name='edit_region'),
    path('region/delete/<int:pk>', views.delete_region, name='delete_region'),

    path('city/add', views.create_city, name='create_city'),
    path('city/edit/<int:pk>', views.edit_city, name='edit_city'),
    path('city/delete/<int:pk>', views.delete_city, name='delete_city'),

]
