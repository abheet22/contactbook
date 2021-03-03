from django.urls import path
from contacts.api.contacts import (
    GetContacts,
    CreateContacts,
    UpdateContacts,
    DeleteContacts
)


urlpatterns = [
    path("get-contacts/", GetContacts.as_view()),
    path("create-contacts/", CreateContacts.as_view()),
    path("update-contacts/<uuid:id>/", UpdateContacts.as_view()),
    path("delete-contacts/<uuid:id>/", DeleteContacts.as_view())
    ]