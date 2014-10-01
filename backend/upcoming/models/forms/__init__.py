import colander as c
from dateutil.parser import *


class FormatDateTime(c.DateTime):
    def serialize(self, node, appstruct):
        if not appstruct:
            return null

        if type(appstruct) is datetime.date:
            appstruct = datetime.datetime.combine(appstruct, datetime.time())

        if not isinstance(appstruct, datetime.datetime):
            raise c.Invalid(node,
                            '"${val}" is not a datetime object',
                            value=appstruct)

        if appstruct.tzinfo is None:
            appstruct = appstruct.replace(tzinfo=self.default_tzinfo)
        return appstruct.strftime(self.format)

    def deserialize(self, node, cstruct):
        if not cstruct:
            return null

        try:
            result = parse(cstruct)
        except Exception:
            raise c.Invalid(node, '"{0}" is an invalid date'.format(cstruct))
        return result

from .users import *
from .upcomings import *

login_schema = LoginSchema()
new_upcoming_schema = NewUpcomingSchema()
