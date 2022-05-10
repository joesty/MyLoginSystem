from django.db import models

# Create your models here.


class Books(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=40, null=False)
    def __str__(self):
        return self.name