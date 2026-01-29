from datetime import datetime
from time import timezone


def unix_now() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())
