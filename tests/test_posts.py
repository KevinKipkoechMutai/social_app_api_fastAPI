from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    assert len(list(posts_map)) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get("/posts/1000")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.id == test_posts[0].content

@pytest.mark.parameterize("title", "content", "published", [
    ("aswesome new title", "awesome new content", True),
    ("aswesome new title 1", "awesome new content 1", True),
    ("aswesome new title 2", "awesome new content 2", False)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]

@pytest.mark.parameterize("title", "content", "published", [
    ("aswesome new title", "awesome new content", True),
    ("aswesome new title 1", "awesome new content 1", True),
    ("aswesome new title 2", "awesome new content 2", False)
])
def test_unauthorized_user_create_post(client, title, content, published):
    res = client.post("/posts/", json={"title": title, "content": content, "published": published})
    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_elete_post_not_exist(authorized_client):
    res = authorized_client.delete(f"/posts/39565847")
    assert res.status_code == 404

