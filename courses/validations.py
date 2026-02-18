from marshmallow import Schema, fields

class CourseSchema(Schema):
    id = fields.Str(dump_only=True)
    c_name = fields.Str(required=True)
    desc = fields.Str()
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)