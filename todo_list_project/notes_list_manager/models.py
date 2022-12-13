from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# class Profile(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     profile_id = models.BigAutoField(primary_key=True)
#
#     def __str__(self):
#         return str(self.user)


class Note(models.Model):
    TYPE_CHOICES = [
        # Ссылка
        ('RF', 'Reference'),
        # Заметка
        ('NT', 'Note'),
        # Памятка
        ('MM', 'Memo'),
        # To do
        ('TD', 'TODO'),
        # …
        ('OT', 'Other')
    ]
    # заголовок
    header = models.CharField(max_length=1000)
    # содержимое(текст с поддержкой базового HTML - форматирования
    content = models.TextField()
    # дату / время создания
    date = models.DateTimeField(default=datetime.now)
    # категорию:
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='NT')
    # отметку “избранная”
    favorite = models.BooleanField(default=False)
    # id
    uuid = models.BigAutoField(primary_key=True)
    # relation with user profile
    # profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.header
