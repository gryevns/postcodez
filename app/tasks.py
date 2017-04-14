import requests

from collections import namedtuple

from rq import get_current_job
from django_rq import job

from app import models


location = namedtuple('Location', 'postcode ward borough')
url = 'http://postcodes.io/postcodes'


def search(postcode):
    r = requests.post(url, json={'postcodes' : [postcode]})
    payload = r.json()
    result = payload.get('result')[0].get('result')
    return location(
        postcode=postcode,
        ward=result.get('admin_ward') if result is not None else None,
        borough=result.get('admin_district') if result is not None else None,
    )


@job
def process(postcode, clean=True):
    job = get_current_job()
    result = search(postcode)
    models.Postcode.objects.update_or_create(
        postcode=result.postcode,
        defaults={
            'ward': result.ward,
            'borough': result.borough,
            'complete': True,
            'deleted': result.ward is None and result.borough is None,
        },
    )
    return 1
