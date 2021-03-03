import copy

from django.conf import settings
from django.test import TestCase

from contacts.tests.base import call_endpoint_for_microservice


class DeleteContactTestCase(TestCase):
    """
    Test cases related to creation of records in contact table
    """

    def setUp(self) -> None:
        """
        Main role of setup is to setup the data for testing and sets endpoints
        :return:
        """
        super(DeleteContactTestCase, self).setUp()
        self.create_endpoint = "/api/v1/contactbook/create-contacts/"
        self.endpoint = "/api/v1/contactbook/delete-contacts/{id}/"
        self.create_method = "POST"
        self.method = "DELETE"
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

    def test_delete_contact_data_id_valid(self):
        create_response = self.create_contact_data()
        self.endpoint = self.endpoint.format(id=create_response["payload"]["id"])
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=None,
            username=self.username,
            password=self.password,
            method=self.method
        )
        self.assertEqual(response["status_code"], 200)

    def test_delete_contact_data_id_invalid(self):
        # create_response = self.create_contact_data()
        self.endpoint = self.endpoint.format(id="f967a846-ae13-447a-8e4d-d8fd3cb6b8a7")
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=None,
            username=self.username,
            password=self.password,
            method=self.method
        )
        self.assertEqual(response["status_code"], 404)
        self.assertEqual(response["message"],
                         "Contact id {} is not present in system".format("f967a846-ae13-447a-8e4d-d8fd3cb6b8a7"))

    def test_delete_contact_data_phone_number_id_invalid(self):
        create_response = self.create_contact_data()
        self.endpoint = self.endpoint.format(id=create_response["payload"]["id"])+\
                        "?flag_delete_number=true&id=586915d7-0242-492c-8434-35b9a92e4eff"
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=None,
            username=self.username,
            password=self.password,
            method=self.method
        )
        self.assertEqual(response["status_code"], 404)
        self.assertEqual(response["error"],
                         "Unable to perform delete operation due to invalid id")

    def test_delete_contact_data_phone_number_id_valid(self):
        create_response = self.create_contact_data()
        extra_params = "?flag_delete_number=true&id={}".format(",".join(create_response["payload"]["nested_ids"]))
        self.endpoint = self.endpoint.format(id=create_response["payload"]["id"])+extra_params
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=None,
            username=self.username,
            password=self.password,
            method=self.method
        )
        self.assertEqual(response["status_code"], 200)

    def test_delete_contact_data_phone_number_id_missing_invalid(self):
        create_response = self.create_contact_data()
        extra_params = "?flag_delete_number=true"
        self.endpoint = self.endpoint.format(id=create_response["payload"]["id"])+extra_params
        response = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=None,
            username=self.username,
            password=self.password,
            method=self.method
        )
        self.assertEqual(response["status_code"], 404)
        self.assertEqual(response["error"],
                         "id is missing for performing delete operation")


