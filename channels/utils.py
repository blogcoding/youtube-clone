import uuid


def get_random_slug():
    code = str(uuid.uuid4())[:24].replace('-', '').lower()
    return code
