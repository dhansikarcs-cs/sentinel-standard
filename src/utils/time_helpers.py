import time
from datetime import datetime, timedelta

def obfuscate_timestamp(current_epoch_ms: int) -> int:
    dt = datetime.fromtimestamp(current_epoch_ms / 1000.0)
    discard = timedelta(minutes=dt.minute % 15, seconds=dt.second, microseconds=dt.microsecond)
    coarse_time = dt - discard
    return int(coarse_time.timestamp() * 1000)
