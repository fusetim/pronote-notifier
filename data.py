from datetime import datetime,timedelta,timezone
from enum import Enum, auto
import re
from hashlib import blake2b

lesson_edit = re.compile('[a-z]+')
lesson_cancel = re.compile('[a-z]+')
lesson_detention = re.compile('[a-z]+')
lesson_teacher_away = re.compile('[a-z]+')
lesson_class_away = re.compile('[a-z]+')


class LessonStatus(Enum):
    Ok = auto()
    Edited = auto()
    Canceled = auto()
    Detention = auto()
    Other = auto()
    TeacherAway = auto()
    ClassAway = auto()

    def __init__(self, _):
        self.inner = None

    def set_inner(self, inner):
        self.inner = inner
        return self

    def get_inner(self):
        return self.inner

    def from_str(status):
        if status is None:
            return LessonStatus.Ok
        else:
            if lesson_edit.match(status):
                return LessonStatus.Edited.set_inner(status)
            if lesson_cancel.match(status):
                return LessonStatus.Canceled.set_inner(status)
            if lesson_detention.match(status):
                return LessonStatus.Detention.set_inner(status)
            if lesson_teacher_away.match(status):
                return LessonStatus.TeacherAway.set_inner(status)
            if lesson_class_away.match(status):
                return LessonStatus.ClassAway.set_inner(status)
            return LessonStatus.Other.set_inner(status)
    
    def __str__(self):
        return self.get_inner()

class Lesson(object):
    def __init__(self, dict):
        self.tfrom = datetime.utcfromtimestamp(dict["from"]//1000)
        self.tto = datetime.utcfromtimestamp(dict["to"]//1000)
        self.subject = dict["subject"]
        self.teacher = dict["teacher"]
        self.room = dict["room"]
        self.status = LessonStatus.from_str(dict["status"])

    def has_room(self):
        return self.room is not None

    def has_status(self):
        return self.status is not None
    
    def has_teacher(self):
        return self.teacher is not None

    def format_from(self):
        return self.tfrom.astimezone().strftime("%d/%m/%Y %Hh%M")

    def format_to(self):
        return self.tfrom.astimezone().strftime("%d/%m/%Y %Hh%M")

    def __str__(self):
        date = self.tfrom.astimezone().strftime("%Y-%m-%d")
        from_ = self.tfrom.astimezone().strftime("%Hh%M")
        to = self.tto.astimezone().strftime("%Hh%M")
        return f"{date}> {from_} - {to}: [{self.subject}] {self.teacher} - {self.room} ({self.status.get_inner()})"

    def __dict__(self):
        tfrom = int(self.tfrom.replace(tzinfo=timezone.utc).timestamp()*1000)
        tto = int(self.tto.replace(tzinfo=timezone.utc).timestamp()*1000)
        return {"from": tfrom, "to": tto, "subject": self.subject, "teacher": self.teacher, "room": self.room, "status": self.status.get_inner()}


    def to_hash(self):
        def stringify_none(value):
            if value:
                return value
            else:
                return "none"
        tfrom = int(self.tfrom.replace(tzinfo=timezone.utc).timestamp()*1000)
        tto = int(self.tto.replace(tzinfo=timezone.utc).timestamp()*1000)
        subject = stringify_none(self.subject)
        teacher = stringify_none(self.teacher)
        room = stringify_none(self.room)
        status = stringify_none(self.status.get_inner())
        concat = f"pronote-notifier_{tfrom}_{tto}_{subject}_{teacher}_{room}_{status}"
        return blake2b(bytes(concat, encoding="utf-8")).hexdigest()