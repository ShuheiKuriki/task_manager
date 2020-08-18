# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Shopping(models.Model):
    name = models.CharField('商品', max_length=256, blank=False)
    shop = models.CharField('店', max_length=256, blank=True)
    price = models.IntegerField('価格', default=0, blank=True, null=True)
    count = models.IntegerField('個数', default=1)
    date = models.DateField('最後に買った日', default=now)
    buy_date = models.DateField('買う日', default=now, null=True)
    past = models.IntegerField('経過日数', blank=True, null=True)
    buy_or_not = models.BooleanField('購入済', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name