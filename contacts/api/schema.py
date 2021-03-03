from marshmallow import fields, ValidationError, pre_load, post_load, validate, post_dump, Schema, validates_schema
from contacts.models import ContactNumber, Contacts

class TrimmedString(fields.String):
    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, "strip"):
            value = value.strip()
        return super()._deserialize(value, *args, **kwargs)


class PhoneNumberSchema(Schema):
    model = ContactNumber

    id = fields.UUID(required=False)
    phone_id = fields.UUID(required=False)

    type = TrimmedString(
        required=True, validate=validate.Length(min=1, max=10, error="Invalid number type provided"),
    )
    number = TrimmedString(
        required=True, validate=validate.Length(min=10, max=10, error="Invalid phone number provided"),
    )
    created_ts = fields.DateTime(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    update_ts = fields.DateTime(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class ContactsSchema(Schema):
    model = Contacts

    id = fields.UUID(required=False)
    name = TrimmedString(
        required=True, validate=validate.Length(min=1, max=20, error="Invalid name provided (length allowed is 20)"),
    )
    email_address = fields.Email(required=True)
    phone_details = fields.Function(
        serialize=lambda obj: PhoneNumberSchema(many=True).dump(obj.contactdetail.all()).data
        if hasattr(obj, "contactdetail")
        else [],
        deserialize=lambda value: PhoneNumberSchema(many=True).load(value).data

    )
    created_ts = fields.DateTime(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    update_ts = fields.DateTime(dump_only=True, format="%Y-%m-%d %H:%M:%S")

    nested_schema = {
        "model":ContactNumber,
        "related":"phone_details",
        "referenced_field":"contact_id",
        "pk":"phone_id"
    }
