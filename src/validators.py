"""Validate units, timestamp, finite values and plausible limits before insert."""
import math
from datetime import datetime, timezone

def validate(row):
    timestamp,temp,humidity,pressure,wind,rain,condition=row
    dt=datetime.fromisoformat(timestamp.replace('Z','+00:00'))
    if dt.tzinfo is None: raise ValueError('Timezone required')
    dt=dt.astimezone(timezone.utc)
    if dt.timestamp()>datetime.now(timezone.utc).timestamp()+300: raise ValueError('Future observation')
    vals=tuple(float(v) for v in (temp,humidity,pressure,wind,rain))
    limits=((-90,65),(0,100),(300,1100),(0,150),(0,500))
    if not all(math.isfinite(v) and lo<=v<=hi for v,(lo,hi) in zip(vals,limits)):
        raise ValueError('Weather measurement outside valid range')
    if not isinstance(condition,str) or not condition.strip(): raise ValueError('Missing condition')
    return (dt.isoformat(timespec='seconds'),*vals,condition.strip())
