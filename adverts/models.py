from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
from django.core.files.images import get_image_dimensions
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from resizeimage import resizeimage
from django_fsm import FSMField, transition
from django.urls import reverse
from accounts.models import CustomUser

IMAGE_SIDE_MIN_SIZE = 300
IMAGE_SIDE_MAX_SIZE = 1500


class Advert(models.Model):
    STATES = [
        ('DR', 'Черновик'),
        ('MO', 'На модерации'),
        ('RE', 'Отклонено, к доработке'),
        ('DE', 'Снято, продано'),
        ('AC', 'Активно')
    ]

    title = models.CharField('Название', max_length=100)
    text = models.TextField('Описание', max_length=5000)
    price = models.DecimalField('Цена', max_digits=11, decimal_places=2)
    views = models.IntegerField('Просмотры', default=0)
    pub_date = models.DateTimeField('Дата публикации', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    category = TreeForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    state = FSMField(default=STATES[0][0], choices=STATES)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('advert_detail', args=[str(self.id)])

    @transition(field=state, source=['DR', 'RE', 'DE'], target='MO')
    def send_on_moderation(self):
        moderators = CustomUser.objects.filter(groups__name='Модераторы')
        if moderators:
            mod_emails = [mod.email for mod in moderators]
            mail_subject = 'Новое объявление требует вашего внимания!'
            message = f'Ссылка на объявление, требующее модерации: http://127.0.0.1:8000/adverts/{self.pk}'
            to_email = mod_emails
            email = EmailMessage(
                mail_subject, message, to=to_email
            )
            email.send()

    @transition(field=state, source='MO', target='RE')
    def mod_reject(self):
        # Отправить пиьсмо пользователю
        pass

    @transition(field=state, source='MO', target='AC')
    def mod_approve(self):
        # Отправить пиьсмо пользователю
        pass

    @transition(field=state, source=['RE', 'AC', 'DE'], target='DR')
    def save_draft(self):
        # Отправить пиьсмо пользователю
        pass

    @transition(field=state, source=['DR', 'RE', 'AC'], target='DE')
    def delete_advert(self):
        # Отправить пиьсмо пользователю
        pass


def img_min_size_validator(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width < IMAGE_SIDE_MIN_SIZE or image_height < IMAGE_SIDE_MIN_SIZE:
        raise ValidationError(
            f'Размер изображения не может быть меньше {IMAGE_SIDE_MIN_SIZE}x{IMAGE_SIDE_MIN_SIZE} пикселей!')


class Image(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    image = models.ImageField('Изображение', upload_to='images/%Y%m%d%H%M%S/', null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'],
                                                         message='Разрешенные расширения изображений: jpg, jpeg, png'),
                                  img_min_size_validator
                              ])

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def save(self, *args, **kwargs):
        pil_image_obj = PILImage.open(self.image)
        width, height = pil_image_obj.size
        if width > IMAGE_SIDE_MAX_SIZE or height > IMAGE_SIDE_MAX_SIZE:
            if width > height:
                new_image = resizeimage.resize_width(pil_image_obj, IMAGE_SIDE_MAX_SIZE)
            else:
                new_image = resizeimage.resize_height(pil_image_obj, IMAGE_SIDE_MAX_SIZE)

            new_image_io = BytesIO()
            new_image.save(new_image_io, format=pil_image_obj.format)

            temp_name = self.image.name
            self.image.delete(save=False)

            self.image.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )

        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.advert.title


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        if not self.slug:
            self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=25)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Region(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class ModNote(models.Model):
    RESOLUTIONS = [
        ('PU', 'Опубликовать'),
        ('RE', 'Отклонить, на доработку'),
    ]
    moderated_at = models.DateTimeField(auto_now=True)
    advert = models.ForeignKey('Advert', on_delete=models.PROTECT, related_name='mod_notes')
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField('Необходимые правки для публикации', max_length=5000, blank=True, null=True)
    resolution = models.CharField(max_length=2, default=RESOLUTIONS[0][0], choices=RESOLUTIONS)

    def __str__(self):
        return self.advert.title

    class Meta:
        verbose_name = 'Запись о модерации'
        verbose_name_plural = 'Записи о модерации'
