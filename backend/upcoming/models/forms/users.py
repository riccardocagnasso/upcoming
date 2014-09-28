import colander as c
import deform as d

class LoginSchema(c.MappingSchema):
    username = c.SchemaNode(c.String())
    password = c.SchemaNode(c.String())
