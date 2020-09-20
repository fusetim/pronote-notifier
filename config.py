import toml

class Settings(object):
    def __init__(self, dict):
        self.api_url = dict["api_url"]
        self.pronote_credentials = PronoteCredentials(dict["credentials"])
        self.webhook = dict["webhook"]

class PronoteCredentials(object):
    def __init__(self, dict):
        self.cas = dict["cas"]
        self.pronote_url = dict["pronote_url"]
        self.username = dict["username"]
        self.password = dict["password"]

class TempStorage(object):
    def __init__(self, dict):
        self.date = dict["date"]
        self.lessons = list(dict["lessons"])
        self.notes = list(dict["notes"])
        self.info = list(dict["info"])

    def __dict__(self):
        return {"date": self.date, "lessons": self.lessons, "notes": self.notes, "info": self.info}

def to_DB(date, lessons = list(), notes = list(), info = list()):
    return TempStorage({"date": date, "lessons": lessons, "notes": notes, "info": info})

def get_settings(path="./config/settings.toml"):
    return Settings(toml.load(path))

def get_db(path="./config/db.toml"):
    return TempStorage(toml.load(path))

def save_db(db, path="./config/db.toml"):
    with open(path, "w") as f:
        return toml.dump(db.__dict__(), f)