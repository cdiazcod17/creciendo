import enum

class Roles(str, enum.Enum):
    user = "user"
    admin = "admin"


class BabySex(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    unknown = "unknown"
    
class EventType(str, enum.Enum):
    feeding = "feeding"
    sleep = "sleep"
    diaper = "diaper"
    bath = "bath"
    
class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"