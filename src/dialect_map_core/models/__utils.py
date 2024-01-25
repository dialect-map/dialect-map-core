# -*- coding: utf-8 -*-

import uuid

from datetime import datetime
from datetime import timezone


def generate_id() -> str:
    """
    Generates a random universal unique identifier (UUID)
    :return: UUID string
    """

    return str(uuid.uuid4()).replace("-", "")


def generate_timestamp() -> datetime:
    """
    Generates a UTC timestamp
    :return: UTC timestamp
    """

    return datetime.now(timezone.utc)
