import pytest
from app.database import Base, engine
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
    user_data = {"email": "test3@gmail.com", "password": "password101", "phone_number": "123455"}
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

@pytest.fixture
def test_posts(test_user, client):
    post_data = [
        {
            "title": "1st post",
            "content": "1st post content",
            "owner_id": test_user["id"]  
        },
        {
            "title": "2nd post",
            "content": "2nd post content",
            "owner_id": test_user["id"]  
        },
        {
            "title": "3rd post",
            "content": "3rd post content",
            "owner_id": test_user["id"]  
        }
    ]
    
    def create_post_model(post):
        models.Post(**post)
    
    post_map = list(map(create_post_model, post_data))
    
    client.add_all(post_map)
    client.commit()
    posts = client.query(models.Post).all()
    return posts