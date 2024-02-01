from app import schemas
from jose import jwt
import pytest

# from app.database import get_db
# from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from app.config import settings

# from alembic import command

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# @pytest.fixture
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)



# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('message') == 'welcome to my first FastAPI app'
#     assert res.status_code == 200
# basic user crud functions

def test_user_create(client):
    res = client.post("/users/", json={"email": "test2@gmail.com", "password": "password101", "phone_number": "123455"})
    newUser = schemas.UserOut(**res.json())
    assert newUser.email == "test2@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password101', 403),
    ('kipkoech@gmail.com', 'wrongcode', 403),
    (None, 'password101', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"