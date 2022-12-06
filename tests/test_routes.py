"""
Wishlist API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import random
from unittest import TestCase
from datetime import datetime
from service import app
from service.models import db, init_db, Wishlist, Item
from service.common import status  # HTTP Status Codes
from tests.factories import WishlistFactory, ItemFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/api/wishlists"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################


# pylint: disable=too-many-public-methods
class TestWishlistService(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_wishlists(self, count, **kwargs):
        """Factory method to create wishlists in bulk"""
        wishlists = []
        for _ in range(count):
            wishlist = WishlistFactory(**kwargs)
            resp = self.client.post(
                BASE_URL, 
                json=wishlist.serialize(),
            )
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Wishlist",
            )
            new_wishlist = resp.get_json()
            wishlist.id = new_wishlist["id"]
            wishlists.append(wishlist)
        return wishlists

    ######################################################################
    #  WISHLIST TEST CASES
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_wishlist(self):
        """It should Create a new wishlist"""
        wishlist = WishlistFactory()
        resp = self.client.post(
            BASE_URL, json=wishlist.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        new_wishlist = resp.get_json()
        self.assertEqual(
            new_wishlist["name"], wishlist.name, "Names does not match"
        )
        self.assertEqual(
            new_wishlist["user_id"], wishlist.user_id, "User ID does not match"
        )
        self.assertEqual(
            new_wishlist["items"], wishlist.items, "Item does not match"
        )
        self.assertEqual(
            new_wishlist["is_enabled"], wishlist.is_enabled, "Is_enabled does not match"
        )

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"], wishlist.name, "Names does not match")
        self.assertEqual(
            new_wishlist["user_id"], wishlist.user_id, "User ID does not match"
        )
        self.assertEqual(
            new_wishlist["items"], wishlist.items, "Item does not match"
        )
        self.assertEqual(
            new_wishlist["is_enabled"], wishlist.is_enabled, "Is_enabled does not match"
        )

    def test_update_wishlist(self):
        """It should Update an already existing wishlist"""
        wishlist = WishlistFactory()
        json = wishlist.serialize()
        resp = self.client.post(
            BASE_URL, json=json, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        wishlist_new = resp.get_json()
        wishlist_id = wishlist_new["id"]
        # name
        wishlist_new["name"] = "newname"
        resp = self.client.put(
            f"{BASE_URL}/{wishlist_id}", json=wishlist_new, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["name"], "newname",
                         "Name is not updated to newname")
        # user_id
        wishlist_new["user_id"] = 123
        resp = self.client.put(
            f"{BASE_URL}/{wishlist_id}", json=wishlist_new, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["user_id"], 123,
                         "user_id is not updated")
        # created_at
        date_time = datetime.now()
        wishlist_new["created_at"] = str(date_time)
        resp = self.client.put(
            f"{BASE_URL}/{wishlist_id}", json=wishlist_new, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        # last_updated
        date_time = datetime.now()
        wishlist_new["last_updated"] = str(date_time)
        resp = self.client.put(
            f"{BASE_URL}/{wishlist_id}", json=wishlist_new, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        # items
        items = [ItemFactory() for _ in range(2)]
        for item in items:
            item.wishlist_id = wishlist_id
        wishlist_new["items"] = [item.serialize() for item in items]
        resp = self.client.put(
            f"{BASE_URL}/{wishlist_id}", json=wishlist_new, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["items"],
                         wishlist_new["items"],
                         "list of items not updated")
        # Sad path when wishlist doesn't exist
        resp = self.client.put(
            f"{BASE_URL}/{12345}", json=wishlist_new, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_clear_wishlist(self):
        """It should Clear items of an already existing wishlist"""
        wishlist = WishlistFactory()
        json = wishlist.serialize()
        resp = self.client.post(
            BASE_URL, json=json, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        wishlist_new = resp.get_json()
        wishlist_id = wishlist_new["id"]
        items = wishlist.items
        self.assertEqual(len(items), 0)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        data = resp.get_json()
        self.assertEqual(len(data['items']), 0)
        random_count = random.randint(1, 10)
        items = []
        for _ in range(random_count):
            item = ItemFactory(wishlist=wishlist, wishlist_id=wishlist_id)
            resp = self.client.post(
                f"{BASE_URL}/{wishlist_id}/items",
                json=item.serialize(),
                content_type="application/json"
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            items.append(item)

        self.assertEqual(len(items), random_count)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}/items", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), random_count)
        for idx, new_item in enumerate(data):
            self.assertEqual(items[idx].id, new_item['id'])
            self.assertEqual(items[idx].name, new_item['name'])
            self.assertEqual(items[idx].wishlist_id, new_item['wishlist_id'])
            self.assertEqual(items[idx].category, new_item['category'])
            self.assertEqual(items[idx].price, new_item['price'])
            self.assertEqual(items[idx].description, new_item['description'])

        resp = self.client.put(
            f"{BASE_URL}/{wishlist_id}/clear", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}/items", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)

        # items
        resp = self.client.put(
            f"{BASE_URL}/{wishlist_id}/clear", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["items"], [],
                         "list of items are not cleared for the given wishlist")

        # Sad path when wishlist doesn't exist
        resp = self.client.put(
            f"{BASE_URL}/{12345}/clear", json=wishlist_new, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_wishlist(self):
        """It should Read a single Wishlist"""
        # get the id of an wishlist
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], wishlist.name)

    def test_get_wishlist_not_found(self):
        """It should not Read an Wishlist that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wishlist(self):
        """It should Delete a Wishlist"""
        # get the id of an wishlist
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_bad_request(self):
        """It should not Create when sending the wrong data"""
        resp = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_all_wishlists_empty(self):
        """It should return empty list of wishlists"""
        resp = self.client.get(
            f"{BASE_URL}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)

    def test_list_all_wishlists(self):
        """It should list all wishlists"""
        random_count = random.randint(1, 10)
        wishlists = self._create_wishlists(random_count)
        resp = self.client.get(
            f"{BASE_URL}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(wishlists))
        for idx, new_wishlist in enumerate(data):
            self.assertEqual(
                new_wishlist["name"], wishlists[idx].name, "Names does not match"
            )
            self.assertEqual(
                new_wishlist["user_id"], wishlists[idx].user_id, "User ID does not match"
            )
            self.assertEqual(
                new_wishlist["items"], wishlists[idx].items, "Item does not match"
            )
            self.assertEqual(
                new_wishlist["is_enabled"], wishlists[idx].is_enabled, "Is_enabled does not match"
            )

    def test_list_all_wishlists_by_user_id(self):
        """It should list all of a users wishlists"""
        random_count = random.randint(1, 10)
        random_user_id = random.randint(1000, 3000)
        wishlists = self._create_wishlists(random_count, user_id=random_user_id)
        resp = self.client.get(
            f"{BASE_URL}?user_id={random_user_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(wishlists))
        for idx, new_wishlist in enumerate(data):
            self.assertEqual(
                new_wishlist["name"], wishlists[idx].name, "Names does not match"
            )
            self.assertEqual(
                new_wishlist["user_id"], wishlists[idx].user_id, "User ID does not match"
            )
            self.assertEqual(
                new_wishlist["items"], wishlists[idx].items, "Item does not match"
            )
            self.assertEqual(
                new_wishlist["is_enabled"], wishlists[idx].is_enabled, "Is_enabled does not match"
            )
            # self.assertEqual(
            #     str(datetime.fromisoformat(new_wishlist["created_at"]).replace(tzinfo=None)),
            #     str(wishlists[idx].created_at.replace(tzinfo=None)),
            #     "created_at does not match",
            # )
            # self.assertEqual(
            #     str(datetime.fromisoformat(new_wishlist["last_updated"]).replace(tzinfo=None)),
            #     str(wishlists[idx].last_updated.replace(tzinfo=None)),
            #     "last_updated does not match",
            # )

    def test_list_all_wishlists_by_name(self):
        """It should list all wishlists with given name"""
        random_count = random.randint(5, 10)
        random_name = "r@ndom_name"
        wishlists = self._create_wishlists(random_count, name=random_name)
        resp = self.client.get(
            f"{BASE_URL}?name={random_name}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(wishlists))
        for idx, new_wishlist in enumerate(data):
            self.assertEqual(
                new_wishlist["name"], wishlists[idx].name, "Names does not match"
            )
            self.assertEqual(
                new_wishlist["user_id"], wishlists[idx].user_id, "User ID does not match"
            )
            self.assertEqual(
                new_wishlist["items"], wishlists[idx].items, "Item does not match"
            )
            self.assertEqual(
                new_wishlist["is_enabled"], wishlists[idx].is_enabled, "Is_enabled does not match"
            )

    def test_list_all_items_in_wishlist(self):
        """It should list all items in given wishlist"""
        wishlist = self._create_wishlists(1)[0]
        wishlist_id = wishlist.id
        items = wishlist.items
        self.assertEqual(len(items), 0)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data['items']), 0)

        random_count = random.randint(1, 10)
        items = []
        for _ in range(random_count):
            item = ItemFactory(wishlist=wishlist, wishlist_id=wishlist_id)
            resp = self.client.post(
                f"{BASE_URL}/{wishlist_id}/items",
                json=item.serialize(),
                content_type="application/json"
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            items.append(item)

        self.assertEqual(len(items), random_count)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}/items", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), random_count)
        for idx, new_item in enumerate(data):
            self.assertEqual(items[idx].id, new_item['id'])
            self.assertEqual(items[idx].name, new_item['name'])
            self.assertEqual(items[idx].wishlist_id, new_item['wishlist_id'])
            self.assertEqual(items[idx].category, new_item['category'])
            self.assertEqual(items[idx].price, new_item['price'])
            self.assertEqual(items[idx].description, new_item['description'])

    def test_list_all_items_in_non_existent_wishlist(self):
        """It should return error 404"""
        random_id = random.randint(1, 100)

        resp = self.client.get(
            f"{BASE_URL}/{random_id}/items", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_items_in_wishlist_by_name(self):
        """It should list all items with a specific name in given wishlist"""
        wishlist = self._create_wishlists(1)[0]
        wishlist_id = wishlist.id
        items = wishlist.items
        self.assertEqual(len(items), 0)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data['items']), 0)

        # test query item by name
        test_name = "testqueryname"
        random_count = random.randint(1, 10)
        items = []
        for _ in range(random_count):
            item = ItemFactory(wishlist=wishlist, wishlist_id=wishlist_id)
            item.name = test_name
            resp = self.client.post(
                f"{BASE_URL}/{wishlist_id}/items",
                json=item.serialize(),
                content_type="application/json"
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            items.append(item)

        # list items with query and make sure that name matches
        self.assertEqual(len(items), random_count)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}/items?name={test_name}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), random_count)
        for idx, new_item in enumerate(data):
            self.assertEqual(items[idx].id, new_item['id'])
            self.assertEqual(test_name, new_item['name'])
            self.assertEqual(items[idx].wishlist_id, new_item['wishlist_id'])

    def test_list_all_items_in_wishlist_by_category(self):
        """It should list all items with a specific category in given wishlist"""
        wishlist = self._create_wishlists(1)[0]
        wishlist_id = wishlist.id
        items = wishlist.items
        self.assertEqual(len(items), 0)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data['items']), 0)

        # test query item by category
        test_category = "testcategory"
        items = []
        total_item_count = 5
        test_count = 3
        for _ in range(total_item_count):
            item = ItemFactory(wishlist=wishlist, wishlist_id=wishlist_id)
            if _ < test_count:
                item.category = test_category
            resp = self.client.post(
                f"{BASE_URL}/{wishlist_id}/items",
                json=item.serialize(),
                content_type="application/json"
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            items.append(item)

        # list items with query and make sure that name matches
        self.assertEqual(len(items), total_item_count)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}/items?category={test_category}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), test_count)
        for idx, new_item in enumerate(data):
            self.assertEqual(items[idx].id, new_item['id'])
            self.assertEqual(items[idx].name, new_item['name'])
            self.assertEqual(items[idx].wishlist_id, new_item['wishlist_id'])
            self.assertEqual(items[idx].category, test_category)

    ######################################################################
    #  ITEM TEST CASES
    ######################################################################

    def test_add_item(self):
        """It should Add an item to a wishlist"""
        wishlist = self._create_wishlists(1)[0]
        item = ItemFactory(wishlist_id=wishlist.id)
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)

        self.assertEqual(data["name"], item.name)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        self.assertEqual(data["category"], item.category)
        self.assertEqual(data["price"], item.price)
        self.assertEqual(data["description"], item.description)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], item.name)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        self.assertEqual(data["category"], item.category)
        self.assertEqual(data["price"], item.price)
        self.assertEqual(data["description"], item.description)

    def test_add_item_not_found(self):
        """It should not Add an item to a wishlist that is not found"""
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/0/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsupported_media_type(self):
        """It should not Create when sending wrong media type"""
        wishlist = WishlistFactory()
        resp = self.client.post(
            BASE_URL, json=wishlist.serialize(), content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_update_item(self):
        """It should Update an item on an wishlist"""
        # create a known address
        wishlist = self._create_wishlists(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["name"] = "XXXX"

        # send the update back
        resp = self.client.put(
            f"{BASE_URL}/{wishlist.id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_item_not_found(self):
        """It should not Update an item that is not found"""
        # create a known address
        wishlist = self._create_wishlists(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        data_id = data["id"]
        data["name"] = "XXXX"

        # send the update back with non-existent id
        resp = self.client.put(
            f"{BASE_URL}/{wishlist.id}/items/0",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # send the update back with non-existent wishlist_id
        resp = self.client.put(
            f"{BASE_URL}/0/items/{data_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item(self):
        """It should Read an Item from a Wishlist"""
        # create a known item
        wishlist = self._create_wishlists(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        self.assertEqual(data["name"], item.name)
        self.assertEqual(data["category"], item.category)
        self.assertEqual(data["price"], item.price)
        self.assertEqual(data["description"], item.description)

    def test_get_item_not_found(self):
        """It should not Read an Item that is not found"""
        resp = self.client.get(f"{BASE_URL}/0/items/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item_wishlist_not_found(self):
        """It should not Read an Item with incorrect Wishlist"""
        # create a known item
        wishlist = self._create_wishlists(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # retrieve it with an incorrect wishlist id
        resp = self.client.get(
            f"{BASE_URL}/0/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_item_in_wishlist(self):
        """It should delete an item in a given wishlist"""
        wishlist = WishlistFactory()
        resp = self.client.post(BASE_URL,
                                json=wishlist.serialize())
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            "Could not create a test Wishlist",
        )
        wishlist_id = resp.get_json()["id"]
        items = wishlist.items
        self.assertEqual(len(items), 0)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        data = resp.get_json()
        self.assertEqual(len(data['items']), 0)

        random_count = random.randint(1, 10)
        items = []
        for _ in range(random_count):
            item = ItemFactory(wishlist=wishlist, wishlist_id=wishlist_id)
            resp = self.client.post(
                f"{BASE_URL}/{wishlist_id}/items",
                json=item.serialize(),
                content_type="application/json"
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            items.append(item)

        self.assertEqual(len(items), random_count)
        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}/items", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), random_count)
        for idx, new_item in enumerate(data):
            self.assertEqual(items[idx].id, new_item['id'])
            self.assertEqual(items[idx].name, new_item['name'])
            self.assertEqual(items[idx].wishlist_id, new_item['wishlist_id'])
            self.assertEqual(items[idx].category, new_item['category'])
            self.assertEqual(items[idx].price, new_item['price'])
            self.assertEqual(items[idx].description, new_item['description'])

        item_id_to_delete = items[0].id
        resp = self.client.delete(
            f"{BASE_URL}/{wishlist_id}/items/{item_id_to_delete}"
        )
        print(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        resp = self.client.get(
            f"{BASE_URL}/{wishlist_id}/items", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), random_count - 1)
        self.assertNotIn(item_id_to_delete, [x["id"] for x in data],
                         f"Couldn't delete {item_id_to_delete}")

        # Sad paths - item doesn't exist in deletion
        resp = self.client.delete(
            f"{BASE_URL}/{wishlist_id}/items/{12341234213}"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # Sad paths - wishlist doesn't exist in deletion
        resp = self.client.delete(
            f"{BASE_URL}/2342343252/items/{item_id_to_delete}"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
