import os
import requests
from dotenv import load_dotenv


LOGIN_URL = "/realms/master/protocol/openid-connect/token"
CREATE_REALM_URL = "/admin/realms"


class KeycloakClient:
    def __init__(self) -> None:
        self.server = os.getenv("KEYCLOAK_SERVER")
        self.realm = os.getenv("KEYCLOAK_REALM")
        self.access_token = None

    def login(self) -> None:
        url = f"{self.server}{LOGIN_URL}"

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        body = {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": os.getenv("KEYCLOAK_ADMIN"),
            "password": os.getenv("KEYCLOAK_ADMIN_PASSWORD"),
        }

        response = requests.post(url=url, headers=headers, data=body)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access_token")
        else:
            raise Exception("login failed.")

    def create_realm(self) -> None:
        url = f"{self.server}{CREATE_REALM_URL}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        body = {
            "id": self.realm,
            "realm": self.realm,
            "displayName": self.realm,
            "enabled": True,
            "sslRequired": "external",
            "registrationAllowed": True,
            "loginWithEmailAllowed": True,
            "duplicateEmailsAllowed": False,
            "resetPasswordAllowed": False,
            "editUsernameAllowed": False,
            "bruteForceProtected": True,
        }

        response = requests.post(url=url, headers=headers, json=body)

        if response.status_code != 201:
            raise Exception("create realm failed")

    def setup(self) -> None:
        self.login()
        self.create_realm()


if __name__ == "__main__":
    load_dotenv()
    client = KeycloakClient()
    client.setup()
