from common.views import ResourceListCreateView, ResourceUpdateDeleteView
from contacts.api.schema import ContactsSchema
from contacts.models import Contacts


class GetContacts(ResourceListCreateView):
    """
        @apiDescription Get contacts details present in the system
        This API could be used to get contact details present in the system. If name or email_address filter is given, it outputs
        all the relevant records that matches those filters.


        @api {get}  /api/v1/contactbook/get-contacts/?name=ramesh1&page=1 GET Contact Details
        @apiversion 1.0.0
        @apiName GET Contact Details
        @apiGroup Contacts

        @apiHeader {String} Authorization: Basic Creds
        @apiHeader {String} Accept-Language Language to accept
        @apiHeader {String} Content-Type application/json

        @apiParam {String} [name] To retrieve contacts which matches the given name
        @apiParam {String}  [email_address] To retrieve contacts which matches the given email_address
        @apiParam {Number} [page] To fetch specific page data.

        @apiSuccessExample {json} Success-Response:
          HTTP/1.1 200 OK
          {
            "response": {
                "message": "Contact information successfully retrieved",
                "payload": [
                    {
                        "email_address": "abheet881.gupta@gmail.com",
                        "phone_details": [
                            {
                                "type": "other",
                                "id": "e387f925-98dd-48ff-a40c-65e88cc1a89d",
                                "created_ts": "2021-03-03 15:36:39",
                                "update_ts": "2021-03-03 15:36:39",
                                "number": "9876543212"
                            }
                        ],
                        "id": "05e845aa-bd16-4db9-a8ef-acee78f596c4",
                        "created_ts": "2021-03-03 15:36:39",
                        "update_ts": "2021-03-03 15:36:39",
                        "name": "abheetg"
                    },
                    {
                        "email_address": "abheet88.gupta@gmail.com",
                        "phone_details": [
                            {
                                "type": "other",
                                "id": "cb779a78-f8de-4240-b255-ad8128161a73",
                                "created_ts": "2021-03-03 15:12:39",
                                "update_ts": "2021-03-03 15:12:39",
                                "number": "9876543212"
                            }
                        ],
                        "id": "123d481b-d57f-4088-a985-dc23d5eac4bb",
                        "created_ts": "2021-03-03 15:12:39",
                        "update_ts": "2021-03-03 15:12:39",
                        "name": "abheetg"
                    },
                    {
                        "email_address": "abheet1211.gupta@gmail.com",
                        "phone_details": [
                            {
                                "type": "mobile",
                                "id": "f967a846-ae13-447a-8e4d-d8fd3cb6b8a7",
                                "created_ts": "2021-03-03 11:52:08",
                                "update_ts": "2021-03-03 11:52:08",
                                "number": "7876543212"
                            },
                            {
                                "type": "mobile",
                                "id": "fbdbc3ce-1e1b-43d1-851e-dcdfa7ec34b7",
                                "created_ts": "2021-03-03 11:51:39",
                                "update_ts": "2021-03-03 11:52:08",
                                "number": "7876543212"
                            }
                        ],
                        "id": "3ed5c809-b956-405e-a111-ff9b55369704",
                        "created_ts": "2021-03-03 08:02:13",
                        "update_ts": "2021-03-03 11:52:08",
                        "name": "ramesh1"
                    },
                    {
                        "email_address": "abheet8811.gupta@gmail.com",
                        "phone_details": [
                            {
                                "type": "other",
                                "id": "135b3df5-95f0-4a3d-921b-c611f71e7b05",
                                "created_ts": "2021-03-03 15:36:51",
                                "update_ts": "2021-03-03 15:36:51",
                                "number": "9876543212"
                            },
                            {
                                "type": "other",
                                "id": "afff921d-9720-4d78-a68a-21e81af31475",
                                "created_ts": "2021-03-03 15:36:51",
                                "update_ts": "2021-03-03 15:36:51",
                                "number": "9876543212"
                            }
                        ],
                        "id": "764f79c2-a530-4950-b958-5d5556b4e555",
                        "created_ts": "2021-03-03 15:36:51",
                        "update_ts": "2021-03-03 15:36:51",
                        "name": "abheetg"
                    },
                    {
                        "email_address": "abheet121.gupta@gmail.com",
                        "phone_details": [
                            {
                                "type": "other",
                                "id": "1285408b-f695-422c-a754-455456a9f434",
                                "created_ts": "2021-03-03 08:01:46",
                                "update_ts": "2021-03-03 08:01:46",
                                "number": "9876543212"
                            }
                        ],
                        "id": "7ea16213-dedc-434d-9c0f-b91ec1169de2",
                        "created_ts": "2021-03-03 08:01:46",
                        "update_ts": "2021-03-03 08:01:46",
                        "name": "abheet"
                    },
                    {
                        "email_address": "abheet12.gupta@gmail.com",
                        "phone_details": [
                            {
                                "type": "mobile",
                                "id": "6ebb2abf-b3e3-411f-8dde-27c7eb13d9f7",
                                "created_ts": "2021-03-03 08:00:03",
                                "update_ts": "2021-03-03 08:00:03",
                                "number": "9876543212"
                            }
                        ],
                        "id": "9224f7de-ad86-4d5b-a2fa-4e3656c5ae10",
                        "created_ts": "2021-03-03 07:59:54",
                        "update_ts": "2021-03-03 07:59:54",
                        "name": "abheet"
                    }
                ],
                "status_code": 200
            },
            "meta": {
                "base": "http://127.0.0.1:8000",
                "next": null,
                "count": 6
            }
        }
        @apiErrorExample {json} Error-Response: get device with invalid name or email_address
            HTTP/1.1 200 OK
            {
        "response": {
            "message": "Contact information successfully retrieved",
            "payload": [],
            "status_code": 200
        },
        "meta": {
            "base": "http://127.0.0.1:8000",
            "next": null,
            "count": 0
        }
    }

    """
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
