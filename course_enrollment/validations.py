from marshmallow import Schema, fields

class EnrollmentSchema(Schema):
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    gender = fields.Str()
    age = fields.Int()
    course_id = fields.Str(required=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    course_name = fields.Str(dump_only=True)
    id = fields.Str(dump_only=True)
    student_id = fields.Str(dump_only=True)

enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)


