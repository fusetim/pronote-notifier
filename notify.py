import requests
from data import LessonStatus

def notify_lesson(webhook, lesson):
    if lesson.status is LessonStatus.Canceled:
        notify_lesson_cancel(webhook.lesson_cancel, lesson)
    if lesson.status is LessonStatus.Ok:
        notify_lesson_add(webhook.lesson_add, lesson)

def notify_lesson_add(url, lesson):
    requests.post(url, data={"value1": lesson.subject, "value2": lesson.format_from(), "value3": lesson.room})

def notify_lesson_cancel(url, lesson):
    requests.post(url, data={"value1": lesson.subject, "value2": lesson.format_from()})
