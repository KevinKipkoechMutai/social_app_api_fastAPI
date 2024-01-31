from typing import List
from app import schemas

def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts/")
    print(res.json())
    # assert len(posts) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_get_all_posts():
    return 

def test_get_one_post():
    return

def test_update_post():
    return

def test_delete_post():
    return