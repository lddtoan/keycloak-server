import os
import http.client as httplib
import requests
from dotenv import load_dotenv
from urllib import parse


LOGIN_URL = "/realms/master/protocol/openid-connect/token"
CREATE_REALM_URL = "/admin/realms"


class KeycloakClient:
    def __init__(self) -> None:
        self.server = os.getenv("KEYCLOAK_SERVER")
        self.realm = os.getenv("KEYCLOAK_REALM")
        self.access_token = None

    def is_online(self) -> bool:
        hostname = parse.urlparse(self.server).hostname
        port = parse.urlparse(self.server).port
        conn = httplib.HTTPConnection(hostname, port, timeout=5)
        for _ in range(5):
            try:
                conn.request("HEAD", "/")
                return True
            except:
                pass
        conn.close()
        return False

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
        if self.is_online():
            self.login()
            self.create_realm()
            print("\nkeycloak-dev run success")
        else:
            print("\ncannot connect to keycloak")
            print("keycloak server may still booting")
            print("you must run this script manually")


if __name__ == "__main__":
    load_dotenv()
    client = KeycloakClient()
    client.setup()
