"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Wishlist
from service.common import status  # HTTP Status Codes
from tests.factories import WishlistFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/wishlists"
######################################################################
#  T E S T   C A S E S
######################################################################
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
        db.session.commit()
        
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    
    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_wishlists(self, count):
        """Factory method to create wishlists in bulk"""
        wishlists = []
        for _ in range(count):
            wishlist = WishlistFactory()
            resp = self.client.post(BASE_URL, json=wishlist.serialize())
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
            new_wishlist["createdAt"],
            str(wishlist.createdAt),
            "createdAt does not match",
        )
        self.assertEqual(
            new_wishlist["lastUpdated"],
            str(wishlist.lastUpdated),
            "lastUpdated does not match",
        )
    

        # # Check that the location header was correct by getting it
        # FIXME: location header not implemented as get_wishlist is not implemented
        # Make sure location header is set
        # location = resp.headers.get("Location", None)
        # self.assertIsNotNone(location)

        # resp = self.client.get(location, content_type="application/json")
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_account = resp.get_json()
        # self.assertEqual(new_account["name"],
        #                  account.name, "Names does not match")
        # self.assertEqual(
        #     new_account["addresses"], account.addresses, "Address does not match"
        # )
        # self.assertEqual(new_account["email"],
        #                  account.email, "Email does not match")
        # self.assertEqual(
        #     new_account["phone_number"], account.phone_number, "Phone does not match"
        # )
        # self.assertEqual(
        #     new_account["date_joined"],
        #     str(account.date_joined),
        #     "Date Joined does not match",
        # )
    
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

    ######################################################################
    #  ITEM TEST CASES
    ######################################################################

    def test_add_item(self):
        """It should Add an item to a wishlist"""
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
        self.assertEqual(data["id"], item.id)
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

        # FIXME when get_item is implemented
        # # retrieve it back
        # resp = self.client.get(
        #     f"{BASE_URL}/{wishlist.id}/items/{item_id}",
        #     content_type="application/json",
        # )
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # data = resp.get_json()
        # logging.debug(data)
        # self.assertEqual(data["id"], item_id)
        # self.assertEqual(data["wishlist_id"], wishlist.id)
        # self.assertEqual(data["name"], "XXXX")

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
        data["name"] = "XXXX"

        # send the update back
        resp = self.client.put(
            f"{BASE_URL}/0/items/0",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
