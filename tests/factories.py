# import datetime
from datetime import date
import factory
import random
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import User, Wishlist, Item

class UserFactory(factory.Factory):
    """Creates fake Users"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    age = random.randint(18, 80)
    address = factory.Faker("address")


class WishlistFactory(factory.Factory):
    """Creates fake Wishlists"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    user_id = factory.SubFactory(UserFactory)
    name = 'Wishlist #'+str(random.randint(1, 100))
    createdAt = FuzzyDate(date(2008, 1, 1))
    lastUpdated = FuzzyDate(date(2008, 1, 1))
        
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
    wishlist_id = factory.SubFactory(WishlistFactory)
    name = FuzzyChoice(choices=["grocery item", "electronic item", "home-care product", "miscellaneous"])
    category = FuzzyChoice(choices=["food", "recreation", "other"])
    price = random.uniform(10, 1000)
    description = factory.Faker("text")