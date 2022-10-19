"""
Wishlist Service


This microservice handles the collection of products of a user wants
"""

from flask import jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Wishlist, Item
import logging

# Import Flask application
from . import app

logger = logging.getLogger("flask.app")


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    data = dict()
    data['description'] = "A RESTful wishlist microservice for ECommerce application"
    data['resources'] = []
    data['resources'].append(
        {
            'method': 'GET',
            'location': '/',
            'description': 'Get details about the APIs'
        }
    )
    data['resources'].append(
        {
            'method': 'POST',
            'location': '/wishlists',
            'description': 'Create a new wishlist'
        }
    )
    data['resources'].append(
        {
            'method': 'GET',
            'location': '/wishlists',
            'description': 'List all wishlists'
        }
    )
    data['resources'].append(
        {
            'method': 'GET',
            'location': '/wishlists/<wishlist_id>',
            'description': 'Read wishlists with id = wishlist_id'
        }
    )
    data['resources'].append(
        {
            'method': 'DELETE',
            'location': '/wishlists/<wishlist_id>',
            'description': 'Delete wishlist with id = wishlist_id'
        }
    )
    data['resources'].append(
        {
            'method': 'PUT',
            'location': '/wishlists/<wishlist_id>',
            'description': 'Update wishlist with id = wishlist_id'
        }
    )
    data['resources'].append(
        {
            'method': 'POST',
            'location': '/wishlists/<wishlist_id>/items',
            'description': 'Add item to wishlist with id = wishlist_id'
        }
    )
    data['resources'].append(
        {
            'method': 'GET',
            'location': '/wishlists/<wishlist_id>/items/<item_id>',
            'description': 'Read item with item_id to wishlist with id = wishlist_id'
        }
    )
    data['resources'].append(
        {
            'method': 'PUT',
            'location': '/wishlists/<wishlist_id>/items/<item_id>',
            'description': 'Update item with item_id to wishlist with id = wishlist_id'
        }
    )
    data['resources'].append(
        {
            'method': 'DELETE',
            'location': '/wishlists/<wishlist_id>/items/<item_id>',
            'description': 'Delete item with item_id to wishlist with id = wishlist_id'
        }
    )
    data['resources'].append(
        {
            'method': 'GET',
            'location': '/wishlists/<wishlist_id>/items',
            'description': 'List all items under wishlist with id = wishlist_id'
        }
    )
    return (
        jsonify(data),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW WISHLIST
######################################################################

@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Creates a Wishlist
    This endpoint will create a Wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create an Wishlist")
    check_content_type("application/json")

    # Create the wishlist
    wishlist = Wishlist()
    wishlist.deserialize(request.get_json())
    wishlist.create()

    # Create a message to return
    message = wishlist.serialize()
    location_url = url_for(
        "get_wishlist", wishlist_id=wishlist.id, _external=True)

    app.logger.info(f"Created Wishlist: {message}")
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL WISHLISTS
######################################################################


@app.route("/wishlists", methods=["GET"])
def get_wishlists():
    """
    List all Wishlists

    This endpoint will return all wishlists belonging to current user
    """
    wishlists = []
    user_id = request.args.get("user_id")
    name = request.args.get("name")
    app.logger.info("Request for all Wishlists")

    if user_id:
        wishlists = Wishlist.find_by_user_id(user_id)
    elif name:
        wishlists = Wishlist.find_by_name(name)
    else:
        wishlists = Wishlist.all()

    result = [wishlist.serialize() for wishlist in wishlists]
    result = sorted(result, key=lambda wishlist: wishlist['id'])
    return make_response(jsonify(result), status.HTTP_200_OK)

######################################################################
# READ A WISHLIST
######################################################################


@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlist(wishlist_id):
    """
    Read a single Wishlist

    This endpoint will return an Wishlist based on it's id
    """
    app.logger.info("Request for Wishlist with id: %s", wishlist_id)

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found.",
        )

    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE A WISHLIST
######################################################################


@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """
    Delete a Wishlist
    This endpoint will delete a Wishlist based the id specified in the path
    """
    app.logger.info("Request to delete wishlist with id: %s", wishlist_id)

    # Retrieve the wishlist to delete and delete it if it exists
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# UPDATE A WISHLIST
######################################################################


@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlist(wishlist_id):
    """
    Update a wishlist
    This endpoint will update a Wishlist based the request body
    """
    logger.info(f"Request to update Wishlist id {wishlist_id}")

    check_content_type("application/json")

    # See if the item exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        logger.error(f"ABORT: Wishlist with id '{wishlist_id}' could not be found.")
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found.",
        )
    else:
        logger.info(f"Wishlist with id {wishlist_id} found")

    # Update from the json in the body of the request
    data = request.get_json()
    wishlist.id = wishlist_id
    wishlist.deserialize(data)
    wishlist.update()

    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


######################################################################
#  ADD AN ITEM TO A WISHLIST
######################################################################


@app.route("/wishlists/<int:wishlist_id>/items", methods=["POST"])
def create_items(wishlist_id):
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
    message = item.serialize()

    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
# READ AN ITEM FROM WISHLIST
######################################################################


@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["GET"])
def get_items(wishlist_id, item_id):
    """
    Get an Item

    This endpoint returns just an Item
    """
    app.logger.info(
        "Request to retrieve Item %s for Wishlist id: %s", (item_id, wishlist_id)
    )

    # See if the item exists and abort if it doesn't
    item = Item.find(item_id)
    if not item or item.serialize()["wishlist_id"] != wishlist_id:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Item with id '{item_id}' for Wishlist id '{wishlist_id}' could not be found.",
        )

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)

######################################################################
# UPDATE AN ITEM
######################################################################


@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["PUT"])
def update_items(wishlist_id, item_id):
    """
    Update an Item
    This endpoint will update an Item based the body that is posted
    """
    app.logger.info(
        "Request to update Item %s for wishlist id: %s", (item_id, wishlist_id)
    )
    check_content_type("application/json")

    # See if the item exists and abort if it doesn't
    item = Item.find(item_id)
    if not item or item.serialize()["wishlist_id"] != wishlist_id:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Item with id '{item_id}' could not be found.",
        )

    # Update from the json in the body of the request
    item.deserialize(request.get_json())
    item.id = item_id
    item.update()

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN ITEM FROM WISHLIST
######################################################################


@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["DELETE"])
def delete_items(wishlist_id, item_id):
    """
    Delete an Item from a wishlist

    """
    app.logger.info(
        "Request to delete Item %s for Wishlist id: %s", (item_id, wishlist_id)
    )
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found.",
        )
    item = Item.find(item_id)
    if not item or item.serialize()["wishlist_id"] != wishlist.id:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Item with id '{item_id}' for Wishlist id '{wishlist_id}' could not be found.",
        )
    wishlist_data = wishlist.serialize()
    # TODO: fix model to avoid this deletion of items in a wishlist
    for item_data in wishlist_data["items"]:
        Item.find(item_data["id"]).delete()
    wishlist_data["items"] = list(filter(lambda x: x["id"] != item_id, wishlist_data["items"]))
    wishlist.deserialize(wishlist_data)
    wishlist.update()
    return make_response(jsonify(item.serialize()), status.HTTP_204_NO_CONTENT)

######################################################################
# LIST ALL ITEMS IN WISHLIST
######################################################################


@app.route("/wishlists/<int:wishlist_id>/items", methods=["GET"])
def list_items(wishlist_id):
    """
    List all items
    This endpoint will list all items in the wishlist
    """
    app.logger.info(
        "Request to list Items for wishlist id: %s", (wishlist_id)
    )

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found.",
        )

    # Update from the json in the body of the request
    result = [item.serialize() for item in wishlist.items]
    result = sorted(result, key=lambda item: item['id'])
    return make_response(jsonify(result), status.HTTP_200_OK)


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
