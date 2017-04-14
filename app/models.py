from django.db import models

from app import managers


class Postcode(models.Model):
    postcode = models.CharField(max_length=6, null=False, db_index=True, unique=True)
    ward = models.CharField(max_length=256, null=True)
    borough = models.CharField(max_length=256, null=True)
    complete = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    objects = managers.PostcodeQuerySet.as_manager()
