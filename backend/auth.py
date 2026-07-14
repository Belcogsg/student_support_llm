import json

USER_FILE = "users.json"


def loading_users():
    with open(USER_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def register_user(username, password):
    users = loading_users()

    if username in users:
        return False

    users[username] = {
        "password": password,
        "role": "student"
    }

    save_users(users)

    return True


def authenticate(username, password):
    users = loading_users()

    if username not in users:
        return False

    if users[username]["password"] == password:
        return True

    return False