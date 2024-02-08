from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def get_token(client: TestClient, email: str, password: str):
    data = {
        'email': email,
        'password': password,
    }
    response = client.post(url='/api/auth/token/login/', data=data)
    user_data = response.json()
    headers = {"Authorization": f"Token {user_data['auth_token']}"}
    return headers


def get_authorized_user(db: Session, client: TestClient, email: str, password: str, username: str, first_name: str, last_name: str):
    data = {
        'email': email,
        'password': password,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
    }
    user = crud.create_user(db, data)
    password = user.get('password')
    email = user.get('email')
    return get_token(client, email, password)
