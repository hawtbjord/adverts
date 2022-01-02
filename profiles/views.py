from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group

from accounts.decorators import allowed_users
from profiles.forms import CreateUserForm, EditUserForm, CategoryForm, RegionForm, CityForm
from adverts.models import Advert, Category, Region, City
from accounts.models import CustomUser
from accounts.email_creds import email_host_user


@login_required(login_url='login')
@allowed_users(allowed_roles=['Пользователи', 'Модераторы', 'Администраторы'])
def profilePage(request):
    if request.user.groups.filter(name='Администраторы'):
        users = CustomUser.objects.all()
        advert_list_to_mod = Advert.objects.filter(state='MO').order_by('updated_at')
        advert_categories = Category.objects.all()
        regions = Region.objects.all()
        cities = City.objects.all()
        template = 'profiles/admin.html'
        context = {'advert_list_to_mod': advert_list_to_mod, 'users': users, 'advert_categories': advert_categories,
                   'regions': regions, 'cities': cities}
    elif request.user.groups.filter(name='Модераторы'):
        advert_list_to_mod = Advert.objects.filter(state='MO').order_by('updated_at')
        template = 'profiles/moderator.html'
        context = {'advert_list_to_mod': advert_list_to_mod}
    elif request.user.groups.filter(name='Пользователи'):
        user_advert_list = Advert.objects.filter(author=request.user)
        template = 'profiles/user.html'
        context = {'user_advert_list': user_advert_list}

    return render(request, template, context)


@allowed_users(allowed_roles=['Администраторы'])
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    return redirect('profile-page')


@allowed_users(allowed_roles=['Администраторы'])
def create_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            groups = form.cleaned_data['groups']
            user = CustomUser.objects.create(email=email, first_name=first_name)

            # ЕСЛИ ГРУППЫ НЕ ВЫБРАНЫ, НАЗНАЧИТЬ ПОЛЬЗОВАТЕЛЯ
            #     my_group = Group.objects.get(name='my_group_name')
            #     my_group.user_set.add(your_user)
            #     user.groups.add(group)
            # else:

            user.save()

            if groups:
                my_group = groups.first()
            else:
                my_group = Group.objects.get(name='Пользователи')
            my_group.user_set.add(user)
            user.groups.add(my_group)

            set_password_form = PasswordResetForm({'email': user.email})
            if set_password_form.is_valid():
                set_password_form.save(
                    request=request,
                    use_https=False,
                    from_email=email_host_user)

            return redirect('profile-page')
    title = 'Создание пользователя'
    context = {'form': form, 'title': title}
    return render(request, 'profiles/ad_create_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def edit_user(request, pk):
    user_instance = get_object_or_404(CustomUser, pk=pk)
    form = EditUserForm(instance=user_instance)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
        return redirect('profile-page')
    title = 'Редактирование пользователя'
    delete_link = "{% url 'delete_user' pk=user_instance.pk %}"
    context = {'form': form, 'user_instance': user_instance, 'title': title, 'delete_link': delete_link}
    return render(request, 'profiles/ad_edit_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def create_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile-page')
    title = 'Создание категории'
    context = {'form': form, 'title': title}
    return render(request, 'profiles/ad_create_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def edit_category(request, slug):
    category_instance = get_object_or_404(Category, slug=slug)
    form = CategoryForm(instance=category_instance)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category_instance)
        if form.is_valid():
            form.save()
        return redirect('profile-page')
    title = 'Редактирование категории'
    context = {'form': form, 'category_instance': category_instance, 'title': title}
    return render(request, 'profiles/ad_edit_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect('profile-page')


@allowed_users(allowed_roles=['Администраторы'])
def create_region(request):
    form = RegionForm()
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile-page')
    title = 'Создание региона'
    context = {'form': form, 'title': title}
    return render(request, 'profiles/ad_create_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def edit_region(request, pk):
    region_instance = get_object_or_404(Region, pk=pk)
    form = RegionForm(instance=region_instance)
    if request.method == "POST":
        form = RegionForm(request.POST, instance=region_instance)
        if form.is_valid():
            form.save()
        return redirect('profile-page')
    title = 'Редактирование регионов'
    context = {'form': form, 'region_instance': region_instance, 'title': title}
    return render(request, 'profiles/ad_edit_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def delete_region(request, pk):
    region = get_object_or_404(Region, pk=pk)
    region.delete()
    return redirect('profile-page')


@allowed_users(allowed_roles=['Администраторы'])
def create_city(request):
    form = CityForm()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile-page')
    title = 'Создание города'
    context = {'form': form, 'title': title}
    return render(request, 'profiles/ad_create_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def edit_city(request, pk):
    city_instance = get_object_or_404(City, pk=pk)
    form = CityForm(instance=city_instance)
    if request.method == "POST":
        form = CityForm(request.POST, instance=city_instance)
        if form.is_valid():
            form.save()
        return redirect('profile-page')
    title = 'Редактирование регионов'
    context = {'form': form, 'region_instance': city_instance, 'title': title}
    return render(request, 'profiles/ad_edit_object.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def delete_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    city.delete()
    return redirect('profile-page')