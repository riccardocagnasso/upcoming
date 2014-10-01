import colander as c
from . import FormatDateTime


class NewUpcomingSchema(c.MappingSchema):
    name = c.SchemaNode(c.String())
    description = c.SchemaNode(c.String())
    date = c.SchemaNode(FormatDateTime())
