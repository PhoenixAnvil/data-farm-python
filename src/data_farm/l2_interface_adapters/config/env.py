import os


def get_user_from_env(username_env: str | None):
    if username_env is not None:
        username = os.environ.get(username_env)
        if not username:
            raise ValueError(f"Could not read username from environment {username_env}.")
        else:
            return username
    else:
        raise ValueError("username_env=None")


def get_password_from_env(password_env: str | None):
    if password_env is not None:
        password = os.environ.get(password_env)
        if not password:
            raise ValueError(f"Could not read password from environment {password_env}.")
        else:
            return password
    else:
        raise ValueError("password_env=None")
