import google.ai.generativelanguage as glm
import requests
import constants

def login(username, password):
    req = requests.post(
        f"{constants.SELF_URL}accounts/create/login",
        json={
            "username": username,
            "password": password
        }
    )
    if req.status_code == 200:
        return {"response": f"the sessionkey for the login is: {req.json()['sessionkey']}. Use this sessionkey in the new requests. Show the actual sesssionkey to user and use it for context in upcoming requests too."}
    else:
        return {"response": req.json()["error"]}

def register(fullname, username, password, email, phone):
    req = requests.post(
        f"{constants.SELF_URL}accounts/create/register",
        json={
            "username": username,
            "password": password,
            "email": email,
            "phone": phone,
            "fullName": fullname
        }
    )
    if req.status_code == 200:
        return {"response": f"account created. ask to login"}
    else:
        return {"response": req.json()["error"]}

def view_self_account(params):
    sessionkey = params
    req = requests.get(
        f"{constants.SELF_URL}accounts/view/self",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        }
    )
    print(req.json())
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

def view_another_account(params):
    try:
        sessionkey, accountID = params.split(",")
    except:
        return {"response": "Invalid properties. requires sessionkey, accountID in this order"}

    req = requests.get(
        f"{constants.SELF_URL}accounts/view/{accountID}",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        }
    )
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

def search_accounts_by_query(params):
    try:
        sessionkey, query = params.split(",")
    except:
        return {"response": "Invalid properties. requires sessionkey, query in this order"}

    req = requests.get(
        f"{constants.SELF_URL}accounts/search/{query}",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        }
    )
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

def set_open_to_work(params):
    sessionkey = params
    req = requests.put(
        f"{constants.SELF_URL}accounts/update/open_to_work",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        }
    )
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

def view_all_skills(params):
    try:
        sessionkey, tagID = params.split(",")
    except:
        return {"response": "Invalid properties. requires sessionkey, tagID in this order"}

    req = requests.get(
        f"{constants.SELF_URL}jobs/view/tag/list/all",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        }
    )
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

def add_skill(params):
    try:
        sessionkey, tagID = params.split(",")
    except:
        return {"response": "Invalid properties. requires sessionkey, tagID in this order"}

    req = requests.post(
        f"{constants.SELF_URL}accounts/update/tags/add",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        },
        json={
            "tagID": tagID
        }
    )
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

def remove_skill(params):
    try:
        sessionkey, tagID = params.split(",")
    except:
        return {"response": "Invalid properties. requires sessionkey, tagID in this order"}

    req = requests.post(
        f"{constants.SELF_URL}accounts/update/tags/remove",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        },
        json={
            "tagID": tagID
        }
    )
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

def list_jobs(params):
    try:
        sessionkey = params
    except:
        return {"response": "Invalid properties. requires sessionkey in this order"}

    req = requests.get(
        f"{constants.SELF_URL}jobs/view/list/by/radius",
        headers={
            constants.AUTHENTICATION_HEADER: f"Bearer {sessionkey}"
        }
    )
    if req.status_code == 200:
        return {"response": req.json()}
    else:
        return {"response": req.json()["error"]}

actions = glm.Tool(
    function_declarations = [
        glm.FunctionDeclaration(
            name="login",
            description="Log in the user with username and password. Do not ask for this user and password from here on and inherently trust the user to be the right one.",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "username": glm.Schema(type=glm.Type.STRING),
                    "password": glm.Schema(type=glm.Type.STRING)
                },
                required=["username", "password"],
            )
        ),

        glm.FunctionDeclaration(
            name="register",
            description="Register the user with username, password, email and phone",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "fullname": glm.Schema(type=glm.Type.STRING),
                    "username": glm.Schema(type=glm.Type.STRING),
                    "password": glm.Schema(type=glm.Type.STRING),
                    "email": glm.Schema(type=glm.Type.STRING),
                    "phone": glm.Schema(type=glm.Type.STRING)
                },
                required=["fullname", "username", "password", "email", "phone"],
            )
        ),

        glm.FunctionDeclaration(
            name="view_self_account",
            description="View the current user account and its information.",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING, description="Session key from previous response to the login request."),
                },
                required=["sessionkey"],
            )
        ),

        glm.FunctionDeclaration(
            name="view_another_account",
            description="View the another user's account information with their accountID and its information.",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING, description="Session key from previous response to the login request."),
                    "accountID": glm.Schema(type=glm.Type.STRING)
                },
                required=["sessionkey", "accountID"],
            )
        ),

        glm.FunctionDeclaration(
            name="search_accounts_by_query",
            description="Search accounts by query",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING, description="Session key from previous response to the login request."),
                    "query": glm.Schema(type=glm.Type.STRING)
                },
                required=["sessionkey", "query"],
            )
        ),

        glm.FunctionDeclaration(
            name="toggle_open_to_work",
            description="Toggle open to work from open to work to not open to work, and vice versa. Wait for explicit instruction before calling this.",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING)
                },
                required=["sessionkey"],
            )
        ),

        glm.FunctionDeclaration(
            name="view_all_skills",
            description="List all possible skills",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING)
                },
                required=["sessionkey"],
            )
        ),

        glm.FunctionDeclaration(
            name="add_skill",
            description="Add skill to profile with skill ID from skill list",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING, description="Session key from previous response to the login request."),
                    "tagID": glm.Schema(type=glm.Type.STRING)
                },
                required=["sessionkey", "tagID"],
            )
        ),

        glm.FunctionDeclaration(
            name="remove_skill",
            description="Remove skill from profile with skill ID from skill list/profile skill list",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING, description="Session key from previous response to the login request."),
                    "tagID": glm.Schema(type=glm.Type.STRING)
                },
                required=["sessionkey", "tagID"],
            )
        ),

        glm.FunctionDeclaration(
            name="list_jobs",
            description="List jobs near me based on last known previous location.",
            parameters=glm.Schema(
                type=glm.Type.OBJECT,
                properties={
                    "sessionkey": glm.Schema(type=glm.Type.STRING)
                },
                required=["sessionkey"],
            )
        )
        
    ],
)