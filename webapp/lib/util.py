import bcrypt


def generate_password_hash(password):
    """Method to centralize the hashing of passwords
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt(12))


def verify_password_hash(password, password_hash):
    """Method to centralize the verification of password hash
    """
    password = password.encode('utf-8')
    password_hash = password_hash.encode('utf-8')
    return bcrypt.hashpw(password, password_hash) == password_hash
