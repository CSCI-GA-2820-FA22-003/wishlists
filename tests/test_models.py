"""
Test cases for YourResourceModel Model

"""
from audioop import add
import os
import logging
import unittest
from service import app
from service.models import PersistentBase, Wishlist, Item, DataValidationError, db
from tests.factories import ItemFactory, WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
class TestYourResourceModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """ It should always be true """
        self.assertTrue(True)

    def test_create_a_wishlist(self):
        """It should Create a Wishlist and assert that it exists"""
        # pylint: disable=unexpected-keyword-arg
        fake_wishlist = WishlistFactory()

        # pylint: disable=unexpected-keyword-arg
        wishlist = Wishlist(
            id = fake_wishlist.id,
            user_id = fake_wishlist.user_id,
            name = fake_wishlist.name,
            createdAt = fake_wishlist.createdAt,
            lastUpdated = fake_wishlist.lastUpdated
        )

        self.assertIsNotNone(wishlist)
        self.assertEqual(wishlist.id, fake_wishlist.id)
        self.assertEqual(wishlist.user_id, fake_wishlist.user_id)
        self.assertEqual(wishlist.name, fake_wishlist.name)
        self.assertEqual(wishlist.createdAt, fake_wishlist.createdAt)
        self.assertEqual(wishlist.lastUpdated, fake_wishlist.lastUpdated)

    def test_add_a_wishlist(self):
        """It should Create a Wishlist and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])

        wishlist = WishlistFactory()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)