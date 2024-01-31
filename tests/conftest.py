import pytest
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.main import app
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
from app import models

@pytest.fixture(scope="session")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head")
    yield TestClient(app)
    # command.downgrade("base")
    
@pytest.fixture(scope="session")
def test_user(client):
    user_data = {"email": "test5@gmail.com", "password": "password101", "phone_number": "123455"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# @pytest.fixture
# def test_user_new(client):
#     user_data = {"email": "test4@gmail.com", "password": "password101", "phone_number": "123455"}
#     res = client.post("/users/", json=user_data)
#     assert res.status_code == 201
#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

# @pytest.fixture
# def test_posts(test_user, db: Session = Depends(get_db)):
#     post_data = [
#         {
#             "title": "1st post",
#             "content": "1st post content"
#         },
#         {
#             "title": "2nd post",
#             "content": "2nd post content"
#         },
#         {
#             "title": "3rd post",
#             "content": "3rd post content" 
#         }
#     ]
    
#     for post in post_data:
#         new_post = models.Post(owner_id = test_user["id"], **post)
#         db.add(new_post)
#         db.commit()
#         db.refresh(new_post)
#     return 