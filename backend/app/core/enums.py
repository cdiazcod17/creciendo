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
    medication = "medication"
    note = "note"
    
class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"