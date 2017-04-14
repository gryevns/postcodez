from django.db import models
from django.db.models import Q


class PostcodeQuerySet(models.QuerySet):

    def complete(self):
        return self.filter(complete=True)

    def invalid(self):
        return self.filter(deleted=True)

    def progress(self):
        complete = self.complete().count()
        return (complete / self.all().count()) * 100 if complete > 0 else 0
