from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'title': 'Главная страница сайта'})
