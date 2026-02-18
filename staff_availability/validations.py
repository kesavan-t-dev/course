from marshmallow import Schema, fields

class StaffAvailabilitySchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    course_id = fields.Str(required=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    reason = fields.Str(allow_none=True)
    id = fields.Str(dump_only=True)
    staff_id = fields.Str(load_default=None)

staff_avail_schema = StaffAvailabilitySchema()

