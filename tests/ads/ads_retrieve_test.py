import pytest


@pytest.mark.django_db
def test_ads_retrieve(client, moderator_token, ad):
    exception_data = {
        "id": ad.pk,
        "name": ad.name,
        "author": ad.author.username,
        "price": 650,
        "category": None,
        "is_published": False
    }

    response = client.get(
        f"/ad/{ad.pk}/",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + moderator_token
    )

    assert response.status_code == 200
    assert response.data == exception_data
