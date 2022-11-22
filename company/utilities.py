import datetime

from crispy_forms.helper import FormHelper
from django.db import models
from django.utils.crypto import get_random_string


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def ShardedDate(sequence):
    shardedUID = str(datetime.datetime.now())
    shardedUID = shardedUID.split('.')
    shardedUID = shardedUID[0].replace('-','').replace(':','').replace(' ','')
    # the shardeduid is built with datetime , tenant ID,
    # le model (sequence) et caractère alphanumérique
    shardedUID = f'{shardedUID}{get_random_string(5).upper()}{sequence[:5].upper()}{get_random_string(5).upper()}'
    return shardedUID


class SlugableModel(models.Model):
    class Meta:
        abstract = True

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug:
            super(SlugableModel, self).save(*args, **kwargs)
        else:
            self.slug = ShardedDate('uuid')
            super(SlugableModel, self).save(*args, **kwargs)


class CommonFormHelper(FormHelper):
    def __init__(self):
        super(CommonFormHelper, self).__init__()
        self.disable_csrf = True
        self.form_tag = False