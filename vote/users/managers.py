from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Менеджер пользовательской модели , в котором login является уникальным
    идентификатором для аутентификации вместо имени пользователя.
    """
    def create_user(self, login, password, **extra_fields):
        """
        Создает пользователя с принятыми login и password.
        """
        if not login:
            raise ValueError('The login must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        if user.is_superuser:
            user.slug = login
        user.save()
        return user

    def create_superuser(self, login, password, **extra_fields):
        """
        Создает суперпользователя с принятыми login и password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(login, password, **extra_fields)
