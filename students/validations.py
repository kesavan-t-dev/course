from marshmallow import Schema, fields

class StudentSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    gender = fields.Str()
    age = fields.Int()


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)