from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Book(models.Model):
    genre_lis = ["小説","アカデミック","テクノロジー","ビジネス","自己啓発"]
    genres=[(i,i) for i in genre_lis]

    title = models.CharField('タイトル', max_length=128)
    genre = models.CharField('ジャンル', choices=genres, default ='小説',max_length=32)
    deadline = models.DateField('期限', default=now, blank=True, null=True)
    expired = models.BooleanField('期限切れ', default=False)

    done_or_not = models.BooleanField(default=False)
    done_date = models.DateField('完了した日', default=now, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField('順番', default=0)

    def __str__(self):
        return self.title

# Create your models here.
