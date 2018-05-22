
from uuid import uuid4


def make_guid():
    guid = str(uuid4()).replace('-', '')
    return 'a' + guid[1:]

