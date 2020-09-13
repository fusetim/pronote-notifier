from config import get_settings
from api import login, logout, get_userinfo

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

    # Log out 
    print("Logout... ", end="")
    logout(session)
    print("Logged out!")

if __name__ == "__main__":
    main()