from config import get_settings, get_db, to_DB, save_db
from api import login, logout, get_userinfo, get_daytimetable
from data import Lesson
from datetime import datetime
from notify import notify_lesson

def main():
    print("Hello World!")
    
    # Load settings
    print("Loading settings... ", end="")
    settings = get_settings()
    print("Loaded!")

    # Log in PronoteApi
    print("Login to PronoteAPI... ", end="")
    session = login(settings.api_url, settings.pronote_credentials)
    print(f"Logged!\nConnected to {settings.api_url} (PronoteAPI).")
    
    user = get_userinfo(session)
    print(f"Logged as {user[0]} ({user[1]}).")

    # Load DB
    print("Loading DB...", end=" ")
    notify, db = load_db()
    print("Loaded!")

    # Get timetable
    print("Itering lessons...")
    timetable = get_daytimetable(session)
    for l in timetable:
        print(str(l), end=" ")
        if l.to_hash() in db.lessons:
            print("(known)")
        else:
            db.lessons.append(l.to_hash())
            if notify:
                notify_lesson(settings.webhook, l)
                print("(new)")
            else:
                print("(new / ignored)")
    print("Ended!")

    # Save DB
    print("Saving DB...", end=" ")
    save_db(db)
    print("Saved!")

    # Log out 
    print("Logout... ", end="")
    logout(session)
    print("Logged out!")


def load_db(): 
    db = None
    notify = True
    try:
        db = get_db()
    except:
        db = None
    today = datetime.now().astimezone().strftime("%Y-%m-%d")
    if db and db.date != today:
        db = None
    if db is None:
        notify = False
        db = to_DB(today)
    return (notify, db)


if __name__ == "__main__":
    main()