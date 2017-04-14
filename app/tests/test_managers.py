import pytest

from app import models


@pytest.mark.django_db
def test_progress():
    models.Postcode.objects.create(postcode=1, deleted=False, complete=False)
    models.Postcode.objects.create(postcode=2, deleted=True, complete=False)
    models.Postcode.objects.create(postcode=3, deleted=False, complete=True)
    models.Postcode.objects.create(postcode=4, deleted=True, complete=True)
    assert models.Postcode.objects.progress() == 50.0
