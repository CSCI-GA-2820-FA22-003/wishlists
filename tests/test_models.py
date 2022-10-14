"""
Test cases for YourResourceModel Model

"""
from audioop import add
import os
import logging
from unicodedata import category, name
import unittest
from service.models import PersistentBase, User, Wishlist, Item, DataValidationError, db
from tests.factories import ItemFactory, UserFactory

######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
class TestYourResourceModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """

    def tearDown(self):
        """ This runs after each test """

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """ It should always be true """
        self.assertTrue(True)

    def test_create_an_item(self):
        """It should Create a User and assert that it exists"""
        # pylint: disable=unexpected-keyword-arg
        fake_user = UserFactory()

        # pylint: disable=unexpected-keyword-arg
        user = User(
            id = fake_user.id,
            name = fake_user.name,
            age = fake_user.age,
            address = fake_user.address
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.id, fake_user.id)
        self.assertEqual(user.name, fake_user.name)
        self.assertEqual(user.age, fake_user.age)
        self.assertEqual(user.address, fake_user.address)

    def test_add_a_user(self):
        """It should Create a User and add it to the database"""
        users = User.all()
        self.assertEqual(users, [])
        # user = User(
        #     name = 'Some username',
        #     age = 30,
        #     address = 'Some address',
        # )

        user = UserFactory()
        user.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(user.id)
        users = User.all()
        self.assertEqual(len(users), 1)