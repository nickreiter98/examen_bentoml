import pytest
import requests
import jwt
from datetime import datetime, timedelta

LOGIN_URL = "http://localhost:8888/login"
PREDICT_URL= "http://localhost:8888/v1/models/uni_acceptance/predict"

CREDENTIALS = {
    "username": "user123",
    "password": "password123"
}

JWT_SECRET_KEY = "123456"
JWT_ALGORITHM = "HS256"

DATA = {
        'gre':340,
        'toefl': 120,
        'uni_rating': 5,
        'sop': 3.5,
        'lor': 4.5,
        'cgpa': 9.5,
        'research': 1
    }


def login():
    response = requests.post(
        url = LOGIN_URL,
        headers={"Content-Type": "application/json"},
        json=CREDENTIALS
    )
    return response.json()['token']



def test_invalid_jwt_token():
    response = requests.post(
        url = LOGIN_URL,
        headers={"Content-Type": "application/json"},
        json={
            "username": "user13",
            "password": "password123"
        }
    )
    assert response.json()['status_code'] == 401 and response.json()['error'] == 'Invalid credentials'

# def test_expired_jwt_token():
#     expiration = (datetime.utcnow() - timedelta(hours=1)).timestamp()
#     payload = {
#         "sub": 'user123',
#         "exp": expiration
#     }
#     token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
#     response = requests.post(
#         PREDICT_URL,
#         headers={
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {token}"
#         },
#         json=DATA
#     )

#     assert response.json()['status_code'] == 401 and response.json()['error'] == 'Token has expired'


def test_valid_request():
    token = login()

    response = requests.post(
        PREDICT_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=DATA
    )
    assert response.json().get('prediction') 

def test_valid_jwt_token():
    token = login()
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    assert payload['sub'] == 'user123'

# def test_jwt_missing():
#     token = login()
#     print(token)
#     token = token[:-1] + 'X'
#     print(token)

#     response = requests.post(
#         PREDICT_URL,
#         headers={
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {token}"
#         },
#         json=DATA
#     )

#     print(response.json())




    
