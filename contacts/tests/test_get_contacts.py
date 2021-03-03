import copy

from django.conf import settings
from django.test import TestCase

from contacts.tests.base import call_endpoint_for_microservice


class GetContactTestCase(TestCase):
    """
    Test cases related to creation of records in contact table
    """

    def setUp(self) -> None:
        """
        Main role of setup is to setup the data for testing and sets endpoints
        :return:
        """
        super(GetContactTestCase, self).setUp()
        self.create_endpoint = "/api/v1/contactbook/create-contacts/"
        self.endpoint = "/api/v1/contactbook/get-contacts/"
        self.create_method = "POST"
        self.method = "GET"
        self.request_data = {
            "name": "abheet",
            "email_address": "abheet.gupta@gmail.com",
            "phone_details": [{"type": "mobile", "number": "9876543212"}]
        }
        self.dupl_data = copy.deepcopy(self.request_data)
        for username, password in settings.BASICAUTH_USERS.items():
            self.username = username
            self.password = password

    def create_contact_data(self):
        return call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.create_endpoint,
            req_data=self.dupl_data,
            username=self.username,
            password=self.password,
            method=self.create_method
        )

    def test_get_contact_data_invalid_credentials(self):
        get_contact_data = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=None,
            username="hello",
            password="hello",
            method=self.method
        )
        self.assertEqual(get_contact_data.status_code, 401)

    def test_get_contact_data_valid(self):
        self.create_contact_data()
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            username=self.username,
            password=self.password,
            req_data=None,
            method=self.method
        )
        self.assertNotEqual(len(response['payload']), 0)
        self.assertEqual(response["status_code"], 200)

    def test_get_contact_search_by_email_valid(self):
        self.create_contact_data()
        self.endpoint = self.endpoint + "?email_address=abheet.gupta@gmail.com"
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            username=self.username,
            password=self.password,
            req_data=None,
            method=self.method
        )
        self.assertNotEqual(len(response['payload']), 0)
        self.assertEqual(response["status_code"], 200)

    def test_get_contact_search_by_name_valid(self):
        self.create_contact_data()
        self.endpoint = self.endpoint + "?name=abheet"
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            username=self.username,
            password=self.password,
            req_data=None,
            method=self.method
        )
        self.assertNotEqual(len(response['payload']), 0)
        self.assertEqual(response["status_code"], 200)

    def test_get_contact_search_by_name_notpresent_valid(self):
        self.create_contact_data()
        self.endpoint = self.endpoint + "?name=rajesh"
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            username=self.username,
            password=self.password,
            req_data=None,
            method=self.method
        )
        self.assertEqual(len(response['payload']), 0)
        self.assertEqual(response["status_code"], 200)

    def test_get_contact_search_by_email_notpresent_valid(self):
        self.create_contact_data()
        self.endpoint = self.endpoint + "?email_address=rajesh.gupta@gmail.com"
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            username=self.username,
            password=self.password,
            req_data=None,
            method=self.method
        )
        self.assertEqual(len(response['payload']), 0)
        self.assertEqual(response["status_code"], 200)

