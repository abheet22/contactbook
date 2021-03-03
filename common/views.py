import json

import django.core.exceptions as dj_core_exceptions
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from common import api_exceptions
from common.basic_auth import basic_auth_required
from common.helpers import build_response
from common.pagination import PageNumberPagination
from contactbook.settings import API_PAGE_SIZE


class ResourceView(View):
    """
    Base class for returning Json response and
    catching API errors
    """
    schema_class = None
    paginator = None
    schema = None
    message = ""

    def __init__(self, *args, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        super(ResourceView, self).__init__(**kwargs)

    def dispatch(self, request, **kwargs):
        if request.body:
            try:
                self.req_data = json.loads(request.body)
            except ValueError:
                raise api_exceptions.BadRequestData(errors="Parse Errors")
        return super(ResourceView, self).dispatch(request, **kwargs)


class ResourceListCreateView(ResourceView):
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = PageNumberPagination
    fields = ()
    max_page_size = API_PAGE_SIZE
    filters = {}

    @method_decorator(api_exceptions.api_exception_handler)
    @method_decorator(basic_auth_required)
    def dispatch(self, request, **kwargs):
        self.schema = self.schema_class()
        self.paginator = self.pagination_class()
        self.paginator.request = request
        return super(ResourceListCreateView, self).dispatch(request, **kwargs)

    def get(self, request, *args, **kwargs):

        queryset = getattr(self, "queryset", self.schema.model.objects.all())
        if getattr(self, "filters", None):
            lookup_dict = {
                lookup: request.GET.get(param) for param, lookup in self.filters.items() if request.GET.get(param)
            }
            queryset = queryset.filter(**{lookup: val for lookup, val in lookup_dict.items() if val})
        paginated_data = self.paginator.paginate_queryset(queryset, self)
        resp_data, errors = self.schema.dump(paginated_data, many=True)
        paginate_response = self.paginator.get_paginated_response(resp_data)
        response = dict()
        response["message"] = self.message
        response["status_code"] = 200
        response["data"] = paginate_response["data"]
        return JsonResponse(
            {
                "response": build_response(request, "GET", self.message, response_data=paginate_response["data"]),
                "meta": paginate_response["meta"],
            }
        )

    def post(self, request, *args, **kwargs):
        nested_fields = []
        nested_ids = []
        model_inst, errors = self.schema.load(self.req_data)
        if errors:
            raise api_exceptions.BadRequestData(errors=errors)
        if model_inst.get(self.schema.nested_schema["related"]):
            nested_fields.extend(model_inst.get(self.schema.nested_schema["related"]))
            del model_inst[self.schema.nested_schema["related"]]
        try:
            related_object = self.schema.model(**model_inst)
            related_object.clean_save()
        except dj_core_exceptions.ValidationError as e:
            raise api_exceptions.BadRequestData(errors=e.message_dict)
        if nested_fields:
            try:
                for record in nested_fields:
                    record.update({self.schema.nested_schema["referenced_field"]: str(related_object.id)})
                    nested_obj = self.schema.nested_schema["model"](**record)
                    nested_obj.clean_save()
                    nested_ids.append(nested_obj.id)
            except dj_core_exceptions.ValidationError as e:
                raise api_exceptions.BadRequestData(errors=e.message_dict)

        response = JsonResponse(
            {
                "response": build_response(
                    request, response_type="POST", response_text=self.message,
                    response_data={"id": related_object.id, "nested_ids": nested_ids}
                )
            },
            status=201,
        )
        return response

    def put(self, request, *args, **kwargs):
        raise api_exceptions.MethodNotAllowed(method=request.method)

    def delete(self, request, *args, **kwargs):
        raise api_exceptions.MethodNotAllowed(method=request.method)


class ResourceUpdateDeleteView(ResourceView):
    http_method_names = ["put", "delete"]
    lookup_field = None

    @method_decorator(api_exceptions.api_exception_handler)
    @method_decorator(basic_auth_required)
    def dispatch(self, request, **kwargs):
        self.schema = self.schema_class()
        return super(ResourceUpdateDeleteView, self).dispatch(request, **kwargs)

    @staticmethod
    def process_data(model, id, update_payload, *args, **kwargs):
        update_fields = ["update_ts"]
        errors = None
        model_obj = model.objects.filter(id=id)
        if model_obj:
            model_obj = model_obj[0]
            for key, value in update_payload.items():
                if hasattr(model_obj, key):
                    update_fields.append(key)
                setattr(model_obj, key, value)
        else:
            errors = "Contact id {} is not present in system".format(id)
        return model_obj, update_fields, errors

    def put(self, request, id, *args, **kwargs):
        nested_fields = []
        model_inst, errors = self.schema.load(self.req_data, partial=True)
        if errors:
            api_exceptions.BadRequestData(errors=errors)
        if model_inst.get(self.schema.nested_schema["related"]):
            nested_fields.extend(model_inst.get(self.schema.nested_schema["related"]))
            del model_inst[self.schema.nested_schema["related"]]
        model_obj, update_fields, errors = self.process_data(self.schema.model, id, model_inst)
        if errors:
            raise api_exceptions.BadRequestData(errors=errors)
        try:
            model_obj.clean_save(update_fields=update_fields)
        except dj_core_exceptions.ValidationError as e:
            raise api_exceptions.BadRequestData(errors=e.message_dict)
        if nested_fields:
            errors_detail = []
            try:
                for record in nested_fields:
                    pk = self.schema.nested_schema["pk"]
                    if pk in record:
                        model_obj, update_fields, errors = self.process_data(self.schema.nested_schema["model"],
                                                                             record[pk], record)
                        if errors:
                            errors_detail.append(errors)
                        else:
                            model_obj.clean_save(update_fields=update_fields)
                    else:
                        record.update({self.schema.nested_schema["referenced_field"]: id})
                        self.schema.nested_schema["model"](**record).clean_save()
            except dj_core_exceptions.ValidationError as e:
                errors_detail.append(e.message_dict)
            if errors:
                raise api_exceptions.BadRequestData(errors=errors_detail)
        response = JsonResponse(
            {
                "response": build_response(
                    request, response_type="PUT", response_text=self.message
                )
            },
            status=202,
        )
        return response

    def delete(self, request, id, *args, **kawrgs):
        model_obj = self.schema.model.objects.filter(id=id)
        if not model_obj:
            raise api_exceptions.NotFound("Contact id {} is not present in system".format(id))
        if request.GET.get(self.lookup_field):
            if request.GET.get("id"):
                model_obj = self.schema.nested_schema["model"].objects.filter(id__in=request.GET.get("id").split(","))
                if model_obj:
                    model_obj.delete()
                else:
                    raise api_exceptions.NotFound(errors="Unable to perform delete operation due to invalid id")
            else:
                raise api_exceptions.NotFound(errors="id is missing for performing delete operation")
        else:
            model_obj.delete()
        return JsonResponse(
            {
                "response": build_response(request, "GET", self.message)
            }
        )
