from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
import importlib
from . import punch_cards
from . import closeouts


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
    #slug = models.SlugField(
    #    default='',
    #    editable=False,
    #    max_length=settings.REPORT_TITLE_MAX_LENGTH,
    #)

    def __str__(self):
        return self.name

    def render(self):

        #filename = "punch_cards"
        #report_code = importlib.import_module("punch_cards", package="src")
        #Todo make dynamic
        #HTML = importlib.import_module(filename, package=None)

        HTML = "No HTML provided"

        if(self.source == "punch-cards"):
            source = punch_cards

        if(self.source == "closeouts"):
            source = closeouts

        HTML = source.rendercode()

        #return "Hi"
        return HTML

    #def get_absolute_url(self):
    #    kwargs = {
    #        'pk': self.id,
    #        'slug': self.slug
    #    }
    #    return reverse('report-pk-slug-etail', kwargs=kwargs)

    #def save(self, *args, **kwargs):
    #    value = self.title
    #    self.slug = slugify(value, allow_unicode=True)
    #    super().save(*args, **kwargs)