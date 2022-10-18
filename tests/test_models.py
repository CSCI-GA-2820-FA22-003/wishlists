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

    def test_read_a_wishlist(self):
        """It should Read a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()

        # Read it back
        found_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(found_wishlist.id, wishlist.id)
        self.assertEqual(found_wishlist.user_id, wishlist.user_id)
        self.assertEqual(found_wishlist.name, wishlist.name)
        self.assertEqual(found_wishlist.createdAt, wishlist.createdAt)
        self.assertEqual(found_wishlist.lastUpdated, wishlist.lastUpdated)
        self.assertEqual(found_wishlist.items, [])

    def test_update_a_wishlist(self):
        """It should Update a Wishlist"""
        wishlist = WishlistFactory(name="Wishlist")
        wishlist.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        self.assertEqual(wishlist.name, "Wishlist")

        # Fetch it back
        wishlist = Wishlist.find(wishlist.id)
        wishlist.name = "My Wishlist"
        wishlist.update()

        # Fetch it back again
        wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(wishlist.name, "My Wishlist")

    def test_delete_a_wishlist(self):
        """It should Delete a Wishlist"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        wishlist.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        wishlist.delete()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 0)

    def test_list_all_wishlists(self):
        """It should list all Wishlists in the Database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        for wishlist in WishlistFactory.create_batch(5):
            wishlist.create()
        # Assert that there are 5 wishlists in the database
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 5)

    def test_find_by_name(self):
        """It should Find a Wishlist by name"""
        wishlist = WishlistFactory()
        wishlist.create()

        # Fetch it back by name
        same_wishlist = Wishlist.find_by_name(wishlist.name)[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.name, wishlist.name)

    def test_serialize_a_wishlist(self):
        """It should Serialize a Wishlist"""
        wishlist = WishlistFactory()
        item = ItemFactory()
        wishlist.items.append(item)
        wishlist.create()
        serial_wishlist = wishlist.serialize()
        self.assertEqual(serial_wishlist["id"], wishlist.id)
        self.assertEqual(serial_wishlist["user_id"], wishlist.user_id)
        self.assertEqual(serial_wishlist["name"], wishlist.name)
        self.assertEqual(serial_wishlist["createdAt"], str(wishlist.createdAt))
        self.assertEqual(serial_wishlist["lastUpdated"], str(wishlist.lastUpdated))        
        self.assertEqual(len(serial_wishlist["items"]), 1)

        items = serial_wishlist["items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["wishlist_id"], item.wishlist_id)
        self.assertEqual(items[0]["name"], item.name)
        self.assertEqual(items[0]["category"], item.category)
        self.assertEqual(items[0]["price"], item.price)
        self.assertEqual(items[0]["description"], item.description)

    def test_deserialize_a_wishlist(self):
        """It should Deserialize a wishlist"""
        wishlist = WishlistFactory()
        item = ItemFactory()
        wishlist.items.append(item)
        wishlist.create()
        serial_wishlist = wishlist.serialize()
        new_wishlist = Wishlist()
        new_wishlist.deserialize(serial_wishlist)
        self.assertEqual(new_wishlist.id, wishlist.id)
        self.assertEqual(new_wishlist.user_id, wishlist.user_id)
        self.assertEqual(new_wishlist.name, wishlist.name)
        self.assertEqual(new_wishlist.createdAt, str(wishlist.createdAt))
        self.assertEqual(new_wishlist.lastUpdated, str(wishlist.lastUpdated))

    def test_deserialize_with_key_error(self):
        """It should not Deserialize a Wishlist with a KeyError"""
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize a Wishlist with a TypeError"""
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, [])

    def test_deserialize_address_key_error(self):
        """It should not Deserialize an Item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_address_type_error(self):
        """It should not Deserialize an Item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    def test_add_wishlist_item(self):
        """It should Create a Wishlist with an Item and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        item = ItemFactory(wishlist=wishlist)
        wishlist.items.append(item)
        wishlist.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

        new_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(new_wishlist.items[0].name, item.name)

        item2 = ItemFactory(wishlist=wishlist)
        wishlist.items.append(item2)
        wishlist.update()

        new_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(new_wishlist.items), 2)
        self.assertEqual(new_wishlist.items[1].name, item2.name)

    def test_update_wishlist_item(self):
        """It should Update an Wishlists item"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])

        wishlist = WishlistFactory()
        item = ItemFactory(wishlist=wishlist)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

        # Fetch it back
        wishlist = Wishlist.find(wishlist.id)
        old_item = wishlist.items[0]
        print("%r", old_item)
        self.assertEqual(old_item.name, item.name)
        # Change the name
        old_item.name = "New name"
        wishlist.update()

        # Fetch it back again
        wishlist = Wishlist.find(wishlist.id)
        item = wishlist.items[0]
        self.assertEqual(item.name, "New name")

    def test_delete_wishlist_item(self):
        """It should Delete a Wishlist Item"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])

        wishlist = WishlistFactory()
        item = ItemFactory(wishlist=wishlist)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

        # Fetch it back
        wishlist = Wishlist.find(wishlist.id)
        item = wishlist.items[0]
        item.delete()
        wishlist.update()

        # Fetch it back again
        wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(wishlist.items), 0)