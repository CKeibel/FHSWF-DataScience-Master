from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Tag:
    sensors: list
    address: str
    name: str
    last_contact: str | datetime
    online: bool

@dataclass
class Gateway:
    network_segment: int
    last_contact: str
    online: bool
    ip_address: str
    id: str # id is keyword in python, maybe needs a mapping
    tags: list[Tag] = field(default_factory = list)