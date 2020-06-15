# Django Multiple DB Idempotency Test

This repo tests whether is it possible to have atomic transactions 
span multiple distinct databases, and whether rollback happens correctly
when a nested transaction fails. 

The tests occur in `test.py` and assert that with two distinct `sqlite3`
databases, models are successfully created, and rolledback on fail.

## Setup
After running pipenv and installing `pytest` from the lockfile:
```
./manage.py migrate && ./manage.py migrate --database=secondary 
```
The tests are then run with:
```
pytest retailer/tests.py
```