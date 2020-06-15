import pytest

from django.db import transaction, IntegrityError

from retailer import models


@pytest.fixture(autouse=True)
def clean():
    models.Retailer.objects.using("default").all().delete()
    models.Retailer.objects.using("secondary").all().delete()
    models.Outlet.objects.using("secondary").all().delete()
    models.Outlet.objects.using("default").all().delete()


@pytest.mark.django_db
def test_idempotency_multiple_db_success():
    with transaction.atomic(using="default"):
        with transaction.atomic(using="secondary"):
            retailer = models.Retailer.objects.using("default").create(name="retailer")
            models.Outlet.objects.using("secondary").create(
                name="Outlet 1", retailer_id=retailer.id
            )
            models.Outlet.objects.using("secondary").create(
                name="Outlet 2", retailer_id=retailer.id
            )

    assert models.Retailer.objects.using("default").count() == 1
    assert models.Retailer.objects.using("secondary").count() == 0
    assert models.Outlet.objects.using("secondary").count() == 2
    assert models.Outlet.objects.using("default").count() == 0


@pytest.mark.django_db
def test_idempotency_multiple_db_fail():
    with pytest.raises(IntegrityError):
        with transaction.atomic(using="default"):
            with transaction.atomic(using="secondary"):
                retailer = models.Retailer.objects.using("default").create(
                    name="retailer"
                )
                models.Outlet.objects.using("secondary").create(
                    name="Outlet 1", retailer_id=retailer.id
                )
                raise IntegrityError

    assert models.Retailer.objects.using("default").count() == 0
    assert models.Retailer.objects.using("secondary").count() == 0
    assert models.Outlet.objects.using("secondary").count() == 0
    assert models.Outlet.objects.using("default").count() == 0
