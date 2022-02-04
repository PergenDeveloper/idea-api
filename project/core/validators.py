import re

def validate_username(username: str) -> bool:
    if not username:
        return False
    return len(username.split()) == 1

def validate_email(email: str) -> bool:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(regex, email)