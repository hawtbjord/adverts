# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.db.models import Q

from .forms import AdvertForm, AdvertImagesForm, ModNoteForm
from .models import Advert, Image, City, Category
from .filters import AdvertFilter


def index_view(request):
    categories = Category.objects.filter(parent_id=None)

    return render(request, 'adverts/index.html', {'categories': categories})


def index(request):
    print(request)
    advert_list = Advert.objects.filter(
        state='AC').order_by(
        '-created_at')

    myFilter = AdvertFilter(request.GET, queryset=advert_list)
    print(myFilter.qs)
    print(request.GET)
    advert_list = myFilter.qs
    advert_list.filter()

    context = {'advert_list': advert_list, 'myFilter': myFilter}
    return render(request, 'adverts/adverts.html', context)


def show_categories(request):
    return render(request, "adverts/categories.html", {'categories': Category.objects.all()})


def load_cities(request):
    region_id = request.GET.get('region')
    cities = City.objects.filter(region_id=region_id)
    return render(request, 'adverts/adverts_cities.html', {'cities': cities})


def detail(request, pk):
    advert = get_object_or_404(Advert, pk=pk)
    if advert.state in ('DR', 'RE', 'DE', 'MO') and advert.author == request.user:
        return render(request, 'adverts/detail.html', {'advert': advert})

    elif advert.state == 'MO' and (
            request.user.groups.filter(name='Модераторы') or request.user.groups.filter(name='Администраторы')):
        mod_note_form = ModNoteForm()

        if request.method == 'POST':

            mod_note_form = ModNoteForm(request.POST)

            if mod_note_form.is_valid():
                mod_note = mod_note_form.save(commit=False)
                mod_note.advert = advert
                mod_note.moderator = request.user
                mod_note.save()

                if mod_note.resolution == 'RE':
                    advert.mod_reject()

                elif mod_note.resolution == 'PU':
                    advert.mod_approve()

                advert.save()
                return redirect('profile-page')

        context = {'advert': advert, 'mod_note_form': mod_note_form}

        return render(request, 'adverts/detail.html', context)

    elif advert.state == 'AC':
        advert.views += 1
        advert.save()
        return render(request, 'adverts/detail.html', {'advert': advert})
    else:
        raise Http404


def create(request):
    image_formset = modelformset_factory(Image, form=AdvertImagesForm, extra=10)

    adv_form = AdvertForm()
    img_formset = image_formset(queryset=Image.objects.none())

    if request.method == 'POST':

        adv_form = AdvertForm(request.POST, request.FILES)
        img_formset = image_formset(request.POST, request.FILES, queryset=Image.objects.none())

        if adv_form.is_valid() and img_formset.is_valid():
            advert = adv_form.save(commit=False)
            advert.author = request.user
            advert.save()

            for form in img_formset.cleaned_data:
                if form:
                    image = form['image']
                    adv_image = Image(advert=advert, image=image)
                    adv_image.save()

            return redirect('home')

    context = {'adv_form': adv_form, 'img_formset': img_formset}
    return render(request, 'adverts/create.html', context)


def edit(request, pk):
    adv_instance = get_object_or_404(Advert, pk=pk)
    image_formset = modelformset_factory(Image, form=AdvertImagesForm, extra=10, max_num=10)
    if adv_instance.author == request.user and adv_instance.state in ('DR', 'RE', 'AC', 'DE'):

        adv_form = AdvertForm(instance=adv_instance)
        img_formset = image_formset(queryset=Image.objects.filter(advert=adv_instance))

        if request.method == 'POST':

            adv_form = AdvertForm(request.POST, request.FILES, instance=adv_instance)
            img_formset = image_formset(request.POST, request.FILES)

            if adv_form.is_valid() and img_formset.is_valid():
                adv_obj = adv_form.save()
                if adv_obj.state in ('AC', 'RE', 'DE'):
                    adv_obj.save_draft()
                adv_obj.save()
                print(img_formset.cleaned_data)
                current_images = Image.objects.filter(advert=adv_instance)

                print(img_formset.cleaned_data)
                for indx, form in enumerate(img_formset.cleaned_data):
                    if form:
                        if form['id'] is None:
                            image = form['image']
                            adv_image = Image(advert=adv_instance, image=image)
                            adv_image.save()
                        elif not form['image']:
                            adv_image = Image.objects.get(id=request.POST.get('form-' + str(indx) + '-id'))
                            adv_image.delete()
                        else:
                            image = form['image']
                            adv_image = Image(advert=adv_instance, image=image)
                            new_image = Image.objects.get(pk=current_images[indx].id)
                            new_image.image = adv_image.image
                            new_image.save()

                return HttpResponseRedirect(adv_instance.get_absolute_url())
        context = {'adv_form': adv_form, 'img_formset': img_formset, 'adv_instance': adv_instance}
        return render(request, 'adverts/edit.html', context)
    else:
        raise Http404


def delete(request, pk):
    adv_instance = get_object_or_404(Advert, pk=pk)
    adv_instance.delete_advert()
    adv_instance.save()
    return HttpResponseRedirect(adv_instance.get_absolute_url())


def send_to_moderator(request, pk):
    adv_instance = Advert.objects.get(pk=pk)
    adv_instance.send_on_moderation()
    adv_instance.save()
    return HttpResponseRedirect(adv_instance.get_absolute_url())


def approve_and_publish(request, pk):
    pass


def reject_with_note(request, pk):
    pass
