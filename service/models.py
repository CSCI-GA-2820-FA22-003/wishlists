"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    Item.init_db(app)
    Wishlist.init_db(app)


class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


class PersistentBase():
    """
    Class that represents a PersistentBase
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))

    def create(self):
        """
        Creates an entity in the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an entity in the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes an entity from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the entities in the database """
        logger.info("Processing all entities")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds an entity by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all entities with the given name

        Args:
            name (string): the name of the entity you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name.contains(name))

    @classmethod
    def find_by_user_id(cls, user_id: str) -> list:
        """Returns all wishlists that belong to the given user_id

        Args:
            user_id (string): the user_id of the entity you want to match
        """
        logger.info("Processing user_id query for %s ...", user_id)
        return cls.query.filter(cls.user_id == user_id)

    @classmethod
    def find_by_enabled(cls, is_enabled: bool) -> list:
        """Returns all wishlists that's active

        Args:
            is_enabled (boolean): whether the wishlist is enabled or not
        """
        if is_enabled:
            logger.info("Processing enabled query")
        else:
            logger.info("Processing non-enabled query")
        return cls.query.filter(cls.is_enabled == is_enabled)

######################################################################
#  I T E M   M O D E L
######################################################################


class Item(db.Model, PersistentBase):
    """
    Class that represents an Item
    """

    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(
        db.Integer,
        db.ForeignKey("wishlist.id", ondelete="CASCADE"),
        nullable=False)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    price = db.Column(db.Float)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f"<Item {self.name} id=[{self.id}] Wishlist[{self.wishlist_id}]>"

    def serialize(self):
        """Serializes an Item into a dictionary"""
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
        }

    def deserialize(self, data):
        """
        Deserializes an Item from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.wishlist_id = data["wishlist_id"]
            self.name = data["name"]
            self.category = data["category"]
            self.price = data["price"]
            self.description = data["description"]
        except KeyError as error:
            raise DataValidationError("Invalid Item: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained "
                "bad or no data " + error.args[0]
            ) from error
        return self

    @classmethod
    def find_by_category(cls, category):
        """Returns all items with the given category

        Args:
            category (string): the category of the item you want to match
        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)


######################################################################
#  W I S H L I S T   M O D E L
######################################################################
class Wishlist(db.Model, PersistentBase):
    """
    Class that represents a Wishlist
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    items = db.relationship("Item", backref="wishlist", passive_deletes=True)

    def __repr__(self):
        return f"<Wishlist {self.name} id=[{self.id}]>"

    def serialize(self):
        """Serializes a Wishlist into a dictionary"""
        wishlist = {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "is_enabled": self.is_enabled,
            "created_at": str(self.created_at).replace(' ','T'),
            "last_updated": str(self.last_updated).replace(' ','T'),
            "items": [],
        }
        for item in self.items:
            wishlist["items"].append(item.serialize())
        return wishlist

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.id = data.get("id")
            self.user_id = data["user_id"]
            self.is_enabled = data["is_enabled"]
            # handle inner list of items
            items_list = data.get("items")
            for json_item in items_list:
                item = Item()
                item.deserialize(json_item)
                self.items.append(item)

        except KeyError as error:
            raise DataValidationError("Invalid Wishlist: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

# ######################################################################
# #  U S E R   M O D E L
# ######################################################################
# class User(db.Model, PersistentBase):
#     """
#     Class that represents a User
#     """

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     age = db.Column(db.Integer)
#     address = db.Column(db.String(100))
#     wishlists = db.relationship("Wishlist", backref="wishlist", passive_deletes=True)

#     def serialize(self):
#         """Serializes a User into a dictionary"""
#         user = {
#             "id": self.id,
#             "name": self.name,
#             "age": self.age,
#             "address": self.address,
#             "wishlists": [],
#         }
#         for wishlist in self.wishlists:
#             user["wishlists"].append(wishlist.serialize())
#         return user

#     def deserialize(self, data):
#         """
#         Deserializes a User from a dictionary
#         Args:
#             data (dict): A dictionary containing the resource data
#         """
#         try:
#             self.id = data["id"]
#             self.name = data["name"]
#             self.age = data["age"]
#             self.address = data["address"]
#             # handle inner list of items
#             wishlists_list = data.get("wishlists")
#             for json_wishlist in wishlists_list:
#                 wishlist = Wishlist()
#                 wishlist.deserialize(json_wishlist)
#                 self.wishlists.append(wishlist)

#         except KeyError as error:
#             raise DataValidationError("Invalid User: missing " + error.args[0]) from error
#         except TypeError as error:
#             raise DataValidationError(
#                 "Invalid User: body of request contained "
#                 "bad or no data - " + error.args[0]
#             ) from error
#         return self
