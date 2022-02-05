import re

def valid_username_format(username: str) -> bool:
    if not username:
        return False
    return len(username.split()) == 1

def valid_email_format(email: str) -> bool:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(regex, email)

def valid_password(password: str) -> bool:
    return len(password) >= 8