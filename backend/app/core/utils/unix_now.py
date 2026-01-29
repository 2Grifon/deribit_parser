from datetime import UTC, datetime


def unix_now() -> int:
    return int(datetime.now(UTC).timestamp())
