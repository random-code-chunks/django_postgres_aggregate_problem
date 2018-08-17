from django.db import models

from example_app.query import RunInfoQuerySet


class RunInfoManager(models.Manager):
    def get_queryset(self):
        return RunInfoQuerySet(self.model)