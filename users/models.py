from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractUser):
    username = models.CharField('Логин', blank=False, unique=True,
                                max_length=40,
                                error_messages={
                                    'unique': 'Такой логин уже есть!',
                                })
    email = models.EmailField('Почта', unique=True, blank=False)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == UserRole.ADMIN


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique')
            ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
