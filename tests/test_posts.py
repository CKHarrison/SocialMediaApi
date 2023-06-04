import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())

    posts_list = list(posts_map)

    def get_post_id(post):
        return post.Post.id
    # sort posts and return them by ascending order based on ID
    sorted_posts = sorted(posts_list, key=get_post_id)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert sorted_posts[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{999}")
    assert res.status_code == 404


@pytest.mark.parametrize('title, content, published', [
    ('This is a title', 'Here is some great content, wow', True),
    ('My favorite beer', 'I have no idea what it is', False),
    ('It is so hot out', 'Cannot leave the house without sweating', True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        '/posts/', json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        '/posts/', json={"title": 'test title', "content": 'some content'})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == 'test title'
    assert created_post.content == 'some content'
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        '/posts/', json={"title": 'test title', "content": 'some content'})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_delete_post_sucess(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f'/posts/{test_posts[0].id}')
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f'/posts/99999')
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f'/posts/{test_posts[3].id}')
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "this post has been updated",
        "content": "this is updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json=data
    )
    # validate that schema is correct
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.id == data['id']


def test_update_other_user_post(authorized_client, test_user, test_another_user, test_posts):
    data = {
        "title": "this post has been updated",
        "content": "this is updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json=data
    )
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "this post has been updated",
        "content": "this is updated content",
        "id": test_posts[3].id
    }
    res = client.put(
        f'/posts/{test_posts[3].id}')
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
      "title": "this post has been updated",
      "content": "this is updated content",
      "id": test_posts[3].id
    }
    res = authorized_client.put(
        f'/posts/99999', json=data)
    assert res.status_code == 404
