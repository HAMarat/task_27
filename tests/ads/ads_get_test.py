import pytest


@pytest.mark.django_db
def test_ads_get(client, ad):
    exception_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author.username,
                "price": 650,
                "category": None,
                "is_published": False
            }
        ]
    }

    response = client.get(
        "/ad/",
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.data == exception_data
