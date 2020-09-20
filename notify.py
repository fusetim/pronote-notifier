import requests
from data import LessonStatus

def notify_lesson(webhook, lesson):
    requests.post(webhook, json={"lesson": prepare_json(lesson)})

def prepare_json(lesson):
    d = lesson.__dict__()
    d["format_from"] = lesson.format_from()
    d["format_to"] = lesson.format_to()
    return d