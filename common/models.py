from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    """
    Abstract BaseModel class
    All models must import from this base model
    """


    exclude_fields = None

    id = models.CharField(primary_key=True, unique=True, editable=False, max_length=36, default=uuid4)
    created_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.id)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj

    def clean_save(self, *args, **kwargs):
        self.full_clean(exclude=self.exclude_fields)
        self.save(*args, **kwargs)