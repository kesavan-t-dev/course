from marshmallow import Schema, fields

class StaffSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)


staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

class StaffRelieveSchema(Schema):
    staff_id = fields.Str(required=True) 
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    reason = fields.Str(required=True)

staff_relieve_schema = StaffRelieveSchema()