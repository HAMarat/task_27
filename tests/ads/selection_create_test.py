import pytest


@pytest.mark.django_db
def test_create_selection(client, moderator_token, ad):
    expected_response = {
        "id": 1,
        "owner": "test_user",
        "name": "Подборка test_user",
        "items": [
            ad.pk
        ]
    }

    data = {
        "owner": "test_user",
        "items": [ad.pk],
        "name": "Подборка test_user"
    }

    response = client.post(
        "/selection/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + moderator_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
