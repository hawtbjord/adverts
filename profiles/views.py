from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group

from accounts.decorators import allowed_users
from profiles.forms import CreateUserForm, EditUserForm
from adverts.models import Advert
from accounts.models import CustomUser
from accounts.email_creds import email_host_user


@login_required(login_url='login')
@allowed_users(allowed_roles=['Пользователи', 'Модераторы', 'Администраторы'])
def profilePage(request):
    if request.user.groups.filter(name='Администраторы'):

        users = CustomUser.objects.all()

        advert_list_to_mod = Advert.objects.filter(state='MO').order_by('updated_at')
        template = 'profiles/admin.html'
        context = {'advert_list_to_mod': advert_list_to_mod, 'users': users}
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

            return redirect('home')
    context = {'form': form}
    return render(request, 'profiles/ad_create_user.html', context)


@allowed_users(allowed_roles=['Администраторы'])
def edit_user(request, pk):
    user_instance = get_object_or_404(CustomUser, pk=pk)
    form = EditUserForm(instance=user_instance)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
        return redirect('profile-page')
    context = {'form': form, 'user_instance': user_instance}
    return render(request, 'profiles/ad_edit_user.html', context)
