from django.db import models

## A model to store a list of which reports the user has installed


class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Report(models.Model):
    name = models.CharField(max_length=200)
    source = models.CharField('The name of the source file that generates the report', max_length=200)
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name