import json
import base64


def call_endpoint_for_microservice(testclient, endpoint,req_data,username,password, method="POST"):
    """
    call endpoint for microservices exists in system
    :param endpoint: API endpoint
    :param req_data: request data
    :param username: basic-auth username
    :param password: basic-auth password
    :return:
    """
    credentials_string = '%s:%s' % (username, password)
    credentials = base64.b64encode(credentials_string.encode())
    auth_headers = {
        'HTTP_AUTHORIZATION': 'Basic ' + credentials.decode(),
    }
    method = method.lower()
    if method in ["post", "put"]:
        res = getattr(testclient, method)(
            endpoint, json.dumps(req_data), content_type="application/json",**auth_headers)
    elif method == "get":
        res = testclient.get(endpoint, req_data,**auth_headers)
    elif method == "delete":
        res = testclient.delete(
            endpoint, content_type="application/json",**auth_headers)
    else:
        res = None
    if res and res.status_code in range(200, 299):
        if res.status_code == 204:
            response = res
        else:
            response = res.json()["response"]
    elif res.status_code == 401:
        response = res
    else:
        response = res.json()
    return response