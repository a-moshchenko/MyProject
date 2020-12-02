from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Employee
        fields = ('first_name', 'last_name', 'avatar')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = ('first_name',)
