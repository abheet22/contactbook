from django.db import models
from common.models import BaseModel


class Contacts(BaseModel):
    """Contact model."""
    name = models.CharField(max_length=200, db_index=True)
    email_address = models.CharField(max_length=255, db_index=True, unique=True, error_messages={"invalid": "Email already exist in system"})

    def __str__(self):
        return "{name}".format(name=self.name)


class ContactNumber(BaseModel):
        """Phone Number model."""
        PHONE_NUMBER_TYPE_CHOICES = (
            ('home', 'Home'),
            ('mobile', 'Mobile'),
            ('fax', 'Fax'),
            ('work', 'Work'),
            ('other', 'Other')
        )
        type = models.CharField(max_length=10, choices=PHONE_NUMBER_TYPE_CHOICES, default="other")
        contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name="contactdetail")
        number = models.CharField(max_length=15)

