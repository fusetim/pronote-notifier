from datetime import datetime,timedelta

class Lesson(object):
    def __init__(self, dict):
        self.tfrom = datetime.utcfromtimestamp(dict["from"]//1000)
        self.tto = datetime.utcfromtimestamp(dict["to"]//1000)
        self.subject = dict["subject"]
        self.teacher = dict["teacher"]
        self.room = dict["room"]
        self.status = dict["status"]

    def has_room(self):
        return self.room is not None
    
    def has_teacher(self):
        return self.teacher is not None

    def __str__(self):
        date = self.tfrom.astimezone().strftime("%Y-%m-%d")
        from_ = self.tfrom.astimezone().strftime("%Hh%M")
        to = self.tto.astimezone().strftime("%Hh%M")
        return f"{date}> {from_} - {to}: [{self.subject}] {self.teacher} - {self.room} ({self.status})"
