import toml

class Settings(object):
    def __init__(self, dict):
        self.api_url = dict["api_url"]
        self.pronote_credentials = PronoteCredentials(dict["credentials"])
        self.webhook = Webhook(dict["webhook"])

class PronoteCredentials(object):
    def __init__(self, dict):
        self.cas = dict["cas"]
        self.pronote_url = dict["pronote_url"]
        self.username = dict["username"]
        self.password = dict["password"]

class Webhook(object):
    def __init__(self, dict):
        self.lesson_add = dict["lesson_add"]
        self.lesson_edit = dict["lesson_edit"]
        self.lesson_cancel = dict["lesson_cancel"]
        self.lesson_away = dict["lesson_away"]
        self.note_add = dict["note_add"]
        self.info_add = dict["info_add"]

def get_settings(path="./config/settings.toml"):
    return Settings(toml.load(path))