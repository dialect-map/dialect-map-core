# -*- coding: utf-8 -*-

import uuid


def generate_id() -> str:
    """
    Generates a random universal unique identifier (UUID)
    :return: UUID string
    """

    return str(uuid.uuid4()).replace("-", "")
