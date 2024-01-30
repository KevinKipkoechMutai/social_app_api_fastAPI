from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = res.json()
    print(posts)
    assert len(posts) == len(test_posts)
    assert res.status_code == 200