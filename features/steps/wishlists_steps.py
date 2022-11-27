# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa

import os
import requests
from behave import given
from compare import expect

@given('the server is started')
def step_impl(context):
    context.base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200

@given('the following wishlists')
def step_impl(context):
    rest_endpoint = f"{context.BASE_URL}/wishlists"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for wishlist in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{wishlist['id']}")
        expect(context.resp.status_code).to_equal(204)
    for row in context.table:
        payload = {
            "id": row['id'],
            "user_id": row['user_id'],
            "name": row['name'],
            "created_at": row['created_at'],
            "last_updated": row['last_updated'],
            "is_enabled": True,
            "items": []
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)


@given('the following items')
def step_impl(context):
    rest_endpoint = f"{context.BASE_URL}/wishlists"
    #assuming no items since all past wishlists are deleted
    #add all items to the first wishlist
    context.resp = requests.get(rest_endpoint)
    wishlist_id = context.resp.json()[0]['id']
    for row in context.table:
        payload = {
            "id": row['id'],
            "wishlist_id": wishlist_id,
            "name": row['name'],
            "category": row['category'],
            "price": row['price'],
            "description": row['description']
        }
        context.resp = requests.post(f"{rest_endpoint}/{wishlist_id}/items", json=payload)
        expect(context.resp.status_code).to_equal(201)

