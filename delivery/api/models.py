from django.db import models

# Create your models here.
class Delivery(models.Model):
    delivery_partner = models.BigIntegerField()


    def __str__(self) -> str:
        return str(self.delivery_partner)

