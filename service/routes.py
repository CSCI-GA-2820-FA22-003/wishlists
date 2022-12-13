"""
Wishlist Service


This microservice handles the collection of products of a user wants
"""
import logging
from flask import jsonify, request, abort
from flask_restx import Resource, fields, reqparse
from service.common import status  # HTTP Status Codes
from service.models import Wishlist, Item

# Import Flask application
from . import app, api

logger = logging.getLogger("flask.app")

# query string arguments
wishlist_args = reqparse.RequestParser()
wishlist_args.add_argument('name', type=str, required=False, location='args', help='Find the Product by name')
wishlist_args.add_argument('user_id', type=str, required=False, location='args', help='List Products by user id')

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


create_item_model = api.model('Item', {
    'wishlist_id': fields.Integer(required=True, description='The ID of the wishlist in which the item is'),
    'name': fields.String(required=True, description='The name of the item'),
    'category': fields.String(required=True, description='The category of the item'),
    'price': fields.Float(required=True, description='The price of the item'),
    'description': fields.String(required=True, description='The description of the item')
})

item_model = api.inherit(
    'ItemModel',
    create_item_model,
    {
        'id': fields.Integer(readOnly=True, description='The unique id assigned internally by service'),
    }
)

create_model = api.model('Wishlist', {
    'name': fields.String(required=True, description='The name of the Wishlist'),
    'user_id': fields.Integer(required=True, description='The user id of the user that created the wishlist'),
    'is_enabled': fields.Boolean(required=True, description='Is the Wishlist enabled before order is placed?'),
    'items': fields.List(fields.Nested(item_model, description='List of items that the wishlist contains'))
})

wishlist_model = api.inherit(
    'WishlistModel',
    create_model,
    {
        'id': fields.Integer(readOnly=True, description='The unique id assigned internally by service'),
    }
)


######################################################################
#  PATH: /wishlists/{id}
######################################################################
@api.route('/wishlists/<wishlist_id>')
@api.param('wishlist_id', 'The Wishlist identifier')
class WishlistResource(Resource):
    """
    WishlistResource class
    Allows the manipulation of a single Wishlist
    GET /wishlist{id} - Returns a Wishlist with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A WISHLIST
    # ------------------------------------------------------------------
    @api.doc('get_wishlist')
    @api.response(404, 'Wishlist not found')
    @api.marshal_with(wishlist_model)
    def get(self, wishlist_id):
        """
        Retrieve a single Wishlist
        This endpoint will return a Wishlist based on it's id
        """
        app.logger.info("Request for Wishlist with id: %s", wishlist_id)

        # See if the wishlist exists and abort if it doesn't
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' could not be found.",
            )

        return wishlist.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING WISHLIST
    # ------------------------------------------------------------------
    @api.doc('update_wishlist')
    @api.response(400, 'The posted Wishlist data was not valid')
    @api.response(404, 'Wishlist not found')
    @api.expect(wishlist_model)
    @api.marshal_with(wishlist_model)
    def put(self, wishlist_id):
        """
        Update a Wishlist
        This endpoint will update a Wishlist based on the body that is posted
        """
        app.logger.info(
            "Request to update wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Wishlist with id '{wishlist_id}' was not found.")
        app.logger.debug('Payload = %s', api.payload)
        wishlist.deserialize(request.get_json())
        wishlist.id = wishlist_id
        wishlist.update()
        return wishlist.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN WISHLIST
    # ------------------------------------------------------------------
    @api.doc('delete_wishlist')
    @api.response(204, 'Wishlist deleted')
    @api.response(404, 'Wishlist not found')
    def delete(self, wishlist_id):
        """
        Delete a wishlist
        This endpoint will delete a Wishlist based the on id specified in the path
        """
        app.logger.info("Request to delete wishlist with id: %s", wishlist_id)

        # Retrieve the wishlist to delete and delete it if it exists
        wishlist = Wishlist.find(wishlist_id)
        if wishlist:
            for item in wishlist.items:
                item.delete()
            wishlist.delete()

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /wishlists
######################################################################
@api.route('/wishlists', strict_slashes=False)
class WishlistCollection(Resource):
    """ Handles all interactions with collections of Wishlists """
    # ------------------------------------------------------------------
    # LIST ALL WISHLISTS
    # ------------------------------------------------------------------
    @api.doc('list_wishlists')
    @api.expect(wishlist_args, validate=True)
    @api.marshal_list_with(wishlist_model)
    def get(self):
        """ Returns all of the Wishlists """
        app.logger.info('Request to list Wishlists...')

        wishlists = []
        args = wishlist_args.parse_args()
        user_id = args['user_id']
        name = args['name']
        # user_id = request.args.get("user_id")
        # name = request.args.get("name")
        app.logger.info("Request for all Wishlists")

        if user_id:
            wishlists = Wishlist.find_by_user_id(user_id)
        elif name:
            wishlists = Wishlist.find_by_name(name)
        else:
            wishlists = Wishlist.all()

        result = [wishlist.serialize() for wishlist in wishlists]
        result = sorted(result, key=lambda wishlist: wishlist['id'])
        return result, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW WISHLIST
    # ------------------------------------------------------------------
    @api.doc('create_wishlists')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(wishlist_model, code=201)
    def post(self):
        """
        Creates a Wishlist
        This endpoint will create a Wishlist based the data in the body that is posted

        """
        app.logger.info("Request to create an Wishlist")
        check_content_type("application/json")
        data = request.get_json()
        app.logger.info("Request to create an Wishlist with data: %s", data)

        # Create the wishlist
        wishlist = Wishlist()
        wishlist.deserialize(data)
        wishlist.create()

        # Create a message to return
        message = wishlist.serialize()
        location_url = api.url_for(WishlistResource, wishlist_id=wishlist.id, _external=True)
        app.logger.info(f"Created Wishlist: {message}")
        return wishlist.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /wishlists/<wishlist_id>/items/
######################################################################
@api.route('/wishlists/<wishlist_id>/items/', strict_slashes=False)
@api.param('wishlist_id', 'The Wishlist identifier')
class ItemCollection(Resource):
    """ Handles all interactions with collections of Items"""
    # ------------------------------------------------------------------
    # LIST ALL ITEMS
    # ------------------------------------------------------------------
    @api.doc('list_items')
    @api.marshal_list_with(item_model)
    def get(self, wishlist_id):
        """
        List all items
        This endpoint will list all items in the wishlist
        """
        app.logger.info("Request for all Items for Wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' was not found.")

        results = [item.serialize() for item in wishlist.items]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ITEM
    # ------------------------------------------------------------------
    @api.doc('create_items')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_item_model)
    @api.marshal_with(item_model, code=201)
    def post(self, wishlist_id):
        """
        Adds an item to a wishlist
        This endpoint will add an Item based the data in the body that is posted
        """
        app.logger.info(
            "Request to add an Item for Wishlist with id: %s", wishlist_id)
        check_content_type("application/json")

        # See if the wishlist exists and abort if it doesn't
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' could not be found.",
            )

        # Create an address from the json data
        item = Item()
        item.deserialize(request.get_json())

        # Append the address to the account
        wishlist.items.append(item)
        wishlist.update()

        # Prepare a message to return
        # message = item.serialize()
        location_url = api.url_for(ItemResource, item_id=item.id, wishlist_id=wishlist.id, _external=True)
        app.logger.info("Item for wishlist ID [%s] created.", id)

        return item.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /wishlists/<wishlist_id>/items/<item_id>
######################################################################
@api.route('/wishlists/<wishlist_id>/items/<item_id>')
@api.param('wishlist_id', 'The Wishlist identifier')
@api.param('item_id', 'The Item identifier')
class ItemResource(Resource):
    """
    ItemResource class
    Allows the manipulation of a single wishlist
    """
    # ------------------------------------------------------------------
    # RETRIEVE A ITEM
    # ------------------------------------------------------------------
    @api.doc('get_item')
    @api.response(404, 'Item not found')
    @api.marshal_with(item_model)
    def get(self, wishlist_id, item_id):
        """
        Get an Item

        This endpoint returns just an Item
        """
        app.logger.info("Request for item with id [%s]", item_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' was not found.")
        app.logger.info(item_id)
        item = Item.find(item_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' was not found.")

        app.logger.info("Get item details successful")
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ITEM
    # ------------------------------------------------------------------
    @api.doc('update_item')
    @api.response(404, 'Item not found')
    @api.response(400, 'The posted Item data was not valid')
    @api.expect(item_model)
    @api.marshal_with(item_model)
    def put(self, wishlist_id, item_id):
        """
        Update an Item
        This endpoint will update an Item based the body that is posted
        """
        app.logger.info(
            "Request to update Wishlist %s for Item id: %s", (item_id, wishlist_id)
        )
        check_content_type("application/json")
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, f"Item with id '{wishlist_id}' was not found.")

        # See if the item exists and abort if it doesn't
        item = Item.find(item_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{item_id}' could not be found.",
            )

        # Update from the json in the body of the request
        item.deserialize(api.payload)
        item.id = item_id
        item.update()

        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ITEM
    # ------------------------------------------------------------------
    @api.doc('delete_items')
    @api.response(204, 'Item deleted')
    @api.response(404, 'Wishlist not found')
    def delete(self, wishlist_id, item_id):
        """
        Delete an item
        This endpoint will delete an Wishlist based the id specified in the path
        """

        app.logger.info(
            "Request to delete item with wishlist_id [%s] and item_id [%s]", wishlist_id, item_id)

        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' was not found.")
        item = Item.find(item_id)
        if item:
            item.delete()
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /wishlists/<wishlist_id>/clear
######################################################################
@api.route('/wishlists/<int:wishlist_id>/clear', strict_slashes=False)
class WishlistUtilsCollection(Resource):
    """ Handles all interactions with collections of Wishlists """
    # ------------------------------------------------------------------
    # CLEAR A WISHLIST
    # ------------------------------------------------------------------
    @api.doc('clear_wishlist')
    @api.response(404, 'Wishlist not found')
    @api.marshal_with(wishlist_model)
    def put(self, wishlist_id):
        """
        Clear a Wishlist
        This endpoint will clear the given Wishlist of its items
        """
        app.logger.info(
            "Request to clear wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Wishlist with id '{wishlist_id}' was not found.")
        wishlist.id = wishlist_id
        wishlist_data = wishlist.serialize()
        for item_data in wishlist_data["items"]:
            Item.find(item_data["id"]).delete()
        wishlist = Wishlist.find(wishlist_id)
        return wishlist.serialize(), status.HTTP_200_OK

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""

    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
