from django.utils.translation import gettext as _

def build_response(request, response_type, response_text, id=None, response_data=None):
    """
    Helper function to create a response dict
    :param response_type: Request method type
    :param response_text: Response message text
    :param id: id to be appended to post request
    :param response_data: response payload to be outputted
    :return: dictionary consisting of response
    """

    def inner_func(data):
        resp = list()
        for d in data:
            out = dict()
            for k, v in d.items():
                out[k] = _(v) if isinstance(v, str) else v
            resp.append(out)
        return resp

    response_dict = dict()

    response_dict["message"] = _(response_text)
    if response_data:
        # Check for django translation for conversion
        if isinstance(response_data, dict):
            dat = dict()
            for k, v in response_data.items():
                dat[k] = _(v) if isinstance(v, str) else v
            response_dict["payload"] = dat
        elif isinstance(response_data, list):
            response_dict["payload"] = inner_func(response_data)
        else:
            raise ValueError("Response Format is not valid")
    else:
        response_dict["payload"] = []

    if response_type == "POST":
        if id:
            response_dict.update(id)
        response_dict["status_code"] = 201

    elif response_type == "PUT":
        response_dict["status_code"] = 202

    elif response_type == "DELETE":
        response_dict["status_code"] = 200

    else:
        response_dict["status_code"] = 200

    return response_dict