import requests

def login(api_url, creds):
    body = {"url": creds.pronote_url, "username": creds.username, "password": creds.password, "cas": creds.cas}
    resp = requests.post(api_url+"/auth/login", json=body, headers={"Content-Type": "application/json"});
    resp.raise_for_status()
    token = resp.json()["token"]
    return get_session(api_url, token)


def get_session(api_url, token):
    s = requests.Session()
    s.headers = {"Content-Type": "application/json", "Token": token}
    return (api_url, s)

def logout(session):
    (api_url, s) = session
    resp = s.post(api_url+"/auth/logout")
    resp.raise_for_status()
    return resp.json()["success"]

def get_ql(session, query):
    (api_url, s) = session
    body = {"query": query}
    resp = s.post(api_url+"/graphql", json=body)
    resp.raise_for_status()
    return resp.json()["data"]

def get_userinfo(session):
    user = get_ql(session, "query {user{name,studentClass{name}}}")["user"]
    return (user["name"], user["studentClass"]["name"])
