import colander as c

class LoginSchema(c.MappingSchema):
    username = c.SchemaNode(c.String())
    password = c.SchemaNode(c.String())
