import copy
from contacts.tests.base import call_endpoint_for_microservice
from django.conf import settings
from django.test import TestCase


class CreateContactTestCase(TestCase):
    """
    Test cases related to creation of records in contact table
    """

    def setUp(self) -> None:
        """
        Main role of setup is to setup the data for testing and sets endpoints
        :return:
        """
        super(CreateContactTestCase, self).setUp()
        self.endpoint = "/api/v1/contactbook/create-contacts/"
        self.method = "POST"
        self.request_data = {
            "name":"abheet",
            "email_address":"abheet.gupta@gmail.com",
            "phone_details":[{"type":"mobile", "number":"9876543212"}]
        }
        self.dupl_data = copy.deepcopy(self.request_data)
        for username, password in settings.BASICAUTH_USERS.items():
            self.username = username
            self.password = password

    def create_contact_data(self):
        return call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.dupl_data,
            username=self.username,
            password=self.password,
            method=self.method
        )

    def test_create_contact_data_valid(self):
        response = self.create_contact_data()
        self.assertEqual(response["status_code"], 201)

    def test_create_contact_data_invalid_credentials(self):
        create_contact_data_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.dupl_data,
            username="hello",
            password="hello",
            method=self.method
        )
        self.assertEqual(create_contact_data_resp.status_code, 401)

    def test_create_contact_data_duplicate_email(self):
        self.create_contact_data()
        response = self.create_contact_data()
        self.assertEqual(response["status_code"], 400)
        self.assertEqual(response["error"], {'email_address': 'Contacts with this Email address already exists.'})

    def test_create_contact_data_invalid_name_length(self):
        self.dupl_data["name"] = "rtyuioiuytrtyuioiuytyui"
        response = self.create_contact_data()
        self.assertEqual(response["status_code"], 400)
        self.assertEqual(response["error"], {'name': 'Invalid name provided (length allowed is 20)'})

    def test_create_contact_data_invalid_email(self):
        self.dupl_data["email_address"] = "abheet.com"
        response = self.create_contact_data()
        self.assertEqual(response["status_code"], 400)
        self.assertEqual(response["error"], {'email_address': 'Not a valid email address.'})

    def test_create_contact_data_missing_email(self):
        del self.dupl_data["email_address"]
        response = self.create_contact_data()
        self.assertEqual(response["status_code"], 400)
        self.assertEqual(response["error"], {'email_address': 'Missing data for required field.'})

    def test_create_contact_data_missing_name(self):
        del self.dupl_data["name"]
        response = self.create_contact_data()
        self.assertEqual(response["status_code"], 400)
        self.assertEqual(response["error"], {'name': 'Missing data for required field.'})

    def test_create_contact_data_invalid_method(self):
        self.method = "DELETE"
        response = self.create_contact_data()
        self.assertEqual(response["status_code"], 405)