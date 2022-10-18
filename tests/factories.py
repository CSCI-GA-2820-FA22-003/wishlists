"""
Python library for creating wishlists and items for tests
"""
from datetime import datetime, timezone
import random
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime
from service.models import Wishlist, Item


class WishlistFactory(factory.Factory):
    """Creates fake Wishlists"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    user_id = random.randint(1, 1000)
    name = 'Wishlist #'+str(random.randint(1, 100))
    created_at = FuzzyDateTime(datetime(2008, 1, 1, tzinfo=timezone.utc))
    last_updated = FuzzyDateTime(datetime(2008, 1, 1, tzinfo=timezone.utc))

    @factory.post_generation
    def items(self, create, extracted, **kwargs):   # pylint: disable=method-hidden, unused-argument
        """Creates the items list"""
        if not create:
            return

        if extracted:
            self.items = extracted


class ItemFactory(factory.Factory):
    """Creates fake Items"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""
        model = Item

    id = factory.Sequence(lambda n: n)
    wishlist_id = None
    name = FuzzyChoice(
        choices=["grocery item", "electronic item", "home-care product", "miscellaneous"]
        )
    category = FuzzyChoice(choices=["food", "recreation", "other"])
    price = random.uniform(10, 1000)
    description = "Some description for item # "+str(id)
    wishlist = factory.SubFactory(WishlistFactory)
