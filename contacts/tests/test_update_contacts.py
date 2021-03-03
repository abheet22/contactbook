import copy

from django.conf import settings
from django.test import TestCase

from contacts.tests.base import call_endpoint_for_microservice


class UpdateContactTestCase(TestCase):
    """
    Test cases related to creation of records in contact table
    """

    def setUp(self) -> None:
        """
        Main role of setup is to setup the data for testing and sets endpoints
        :return:
        """
        super(UpdateContactTestCase, self).setUp()
        self.create_endpoint = "/api/v1/contactbook/create-contacts/"
        self.endpoint = "/api/v1/contactbook/update-contacts/{id}/"
        self.get_endpoint = "/api/v1/contactbook/get-contacts/"
        self.create_method = "POST"
        self.get_method = "GET"
        self.method = "PUT"
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

    def test_update_contact_data_id_valid(self):
        create_response = self.create_contact_data()
        self.endpoint = self.endpoint.format(id=create_response["payload"]["id"])
        self.update_params = {"name":"test"}
        call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.update_params,
            username=self.username,
            password=self.password,
            method=self.method
        )
        self.get_endpoint = self.get_endpoint + "?name=test"
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.get_endpoint,
            req_data=None,
            username=self.username,
            password=self.password,
            method=self.get_method
        )
        self.assertEqual(response["status_code"], 200)
        self.assertNotEqual(len(response['payload']), 0)