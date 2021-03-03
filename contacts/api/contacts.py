from common.views import ResourceListCreateView, ResourceUpdateDeleteView
from contacts.api.schema import ContactsSchema
from contacts.models import Contacts

class GetContacts(ResourceListCreateView):
    schema_class = ContactsSchema
    model = Contacts
    queryset = None
    filters = {"name": "name", "email_address": "email_address"}
    fields = ()
    message = "Contact information successfully retrieved"

    def get(self, request, *args, **kwargs):
        self.queryset = (
            self.model.objects.filter()
                .prefetch_related("contactdetail")
        )

        return super(GetContacts, self).get(request, *args, **kwargs)


class CreateContacts(ResourceListCreateView):
    schema_class = ContactsSchema
    model = Contacts
    message = "Contact information successfully created"

class UpdateContacts(ResourceUpdateDeleteView):
    schema_class = ContactsSchema
    model = Contacts
    message = "Contact information successfully updated"

class DeleteContacts(ResourceUpdateDeleteView):
    schema_class = ContactsSchema
    model = Contacts
    lookup_field = "flag_delete_number"
    message = "Contact information successfully deleted"