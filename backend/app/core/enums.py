import enum

class Roles(str, enum.Enum):
    user = "user"
    admin = "admin"


class BabySex(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    unknown = "unknown"