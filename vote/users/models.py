from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager


class Department(models.Model):

    """ Отделы компании """

    name = models.CharField(verbose_name='название', max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('by_category', args=[self.slug])

    class Meta:
        verbose_name = 'отдел'
        verbose_name_plural = 'отделы'


class Employee(AbstractBaseUser, PermissionsMixin):

    """ Сотрудники компании """

    login = models.CharField(max_length=255, unique=True, verbose_name='логин')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    slug = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='media/user_photo',
                               verbose_name='Фото',
                               default='not_available.jpg')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   null=True, blank=True,
                                   verbose_name='Отдел', related_name='users')
    position = models.CharField(max_length=255, verbose_name='Должность', )
    employment = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)

    REQUIRED_FIELD = ['login']
    USERNAME_FIELD = 'login'

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Like(models.Model):

    """ Лайк (голос) """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True,
                                 blank=True, verbose_name='За кого голос',
                                 related_name='likes')
    one_who_votes = models.CharField(max_length=255,
                                     verbose_name='Тот кто голосует')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    description = models.TextField(blank=False, verbose_name='Описание')
