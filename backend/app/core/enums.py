import enum

class BabySex(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    unknown = "unknown"