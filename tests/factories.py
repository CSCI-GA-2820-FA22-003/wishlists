# import datetime
from datetime import datetime, timezone
import factory
import random
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
    createdAt = FuzzyDateTime(datetime(2008, 1, 1, tzinfo=timezone.utc))
    lastUpdated = FuzzyDateTime(datetime(2008, 1, 1, tzinfo=timezone.utc))
        
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
    name = FuzzyChoice(choices=["grocery item", "electronic item", "home-care product", "miscellaneous"])
    category = FuzzyChoice(choices=["food", "recreation", "other"])
    price = random.uniform(10, 1000)
    description = "Some description for item # "+str(id)
    wishlist = factory.SubFactory(WishlistFactory)    