from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('main/', views.index_view, name='index'),

    path('adverts/<int:pk>', views.detail, name='advert_detail'),
    path('adverts/create', views.create, name='create_advert'),
    path('adverts/edit/<int:pk>', views.edit, name='edit_advert'),
    path('adverts/delete/<int:pk>', views.delete, name='delete_advert'),

    path('adverts/<int:pk>/send_to_moderator', views.send_to_moderator, name='send_to_moderator'),
    path('adverts//<int:pk>/publish', views.approve_and_publish, name='approve_and_publish'),
    path('adverts//<int:pk>/reject', views.reject_with_note, name='reject_with_note'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

    path('categories/', views.show_categories, name='show_categories'),

]
