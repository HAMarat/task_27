import pytest


@pytest.mark.django_db
def test_create_ads(client, moderator_token):
    expected_response = {
        "id": 1,
        "name": "test_name_ad",
        "author": "test_user",
        "price": 650,
        "category": None,
        "is_published": False
    }

    data = {
        "name": "test_name_ad",
        "author": "test_user",
        "price": 650,
        "is_published": False
    }

    response = client.post(
        "/ad/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + moderator_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
