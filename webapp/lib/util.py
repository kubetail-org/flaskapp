import bcrypt
from decorator import decorator

from webapp.meta import db


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


def commit_on_success_wrapper(func, *args, **kwargs):
    """Decorator commits transaction on success and issues rollback on
    exceptions. In order for this to work as expected, autocommit must be
    "True" for the session. Otherwise, the top-level commiting function
    must close the session to commit the initial transaction.
    """
    sess = db.Session()

    # to nest or not to nest
    if sess.transaction is None:
        transaction = sess.begin()
    else:
        transaction = sess.begin_nested()

    try:
        result = func(*args, **kwargs)
    except:
        # Always roll back the transaction if something goes wrong
        if transaction.is_active:
            transaction.rollback()
        raise
    else:
        # Success! Commit the transaction if one is active
        if transaction.is_active:
            transaction.commit()

    return result


commit_on_success = decorator(commit_on_success_wrapper)
