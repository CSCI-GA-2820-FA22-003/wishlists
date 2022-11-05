# wishlists

[![Build Status](https://github.com/CSCI-GA-2820-FA22-003/wishlists/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-003/wishlists/actions)

[![codecov](https://codecov.io/github/CSCI-GA-2820-FA22-003/wishlists/branch/main/graph/badge.svg?token=ZOZAX2E6JV)](https://codecov.io/github/CSCI-GA-2820-FA22-003/wishlists)

A RESTful wishlist microservice for ecommerce application

Following routes are available for CRUDL (Create, Read, Update, Delete, List) operations
on a Wishlist and on items in a wishlist:

- Create a wishlists - POST `/wishlists`

```sh
$ curl --location --request POST 'localhost:8000/wishlists' \
> --header 'Content-Type: application/json' \
> --data-raw '{
>     "name": "wishlist1",
>     "id": 123,
>     "user_id": 456,
>     "created_at": "2022-10-19 18:10:23.678271",
>     "last_updated": "2022-10-19 18:10:23.678271",
>     "items": []
> }'
{
  "created_at": "2022-10-19 18:10:23.678271+00:00",
  "id": 6252,
  "items": [],
  "last_updated": "2022-10-19 18:10:23.678271+00:00",
  "name": "wishlist1",
  "user_id": 456
}
```


- Read a Wishlist - GET `/wishlists/<int:wishlist_id>`
```sh
$ curl --location --request GET 'localhost:8000/wishlists/6251' \
> --header 'Content-Type: application/json'
{
  "created_at": "2022-10-19 18:10:23.678271+00:00",
  "id": 6251,
  "items": [],
  "last_updated": "2022-10-19 18:10:23.678271+00:00",
  "name": "wishlist1",
  "user_id": 456
}
```

- Update a Wishlist - PUT `/wishlists/<int:wishlist_id>`
```sh
$ curl --location --request PUT 'localhost:8000/wishlists/6250' \
> --header 'Content-Type: application/json' \
> --data-raw '{
>   "created_at": "2022-10-19 18:10:23.678271+00:00",
>   "id": 6251,
>   "items": [],
>   "last_updated": "2022-10-19 18:10:23.678271+00:00",
>   "name": "wishlist2",
>   "user_id": 456
> }'
{
  "created_at": "2022-10-19 18:10:23.678271+00:00",
  "id": 6251,
  "items": [],
  "last_updated": "2022-10-19 18:10:23.678271+00:00",
  "name": "wishlist2",
  "user_id": 456
}
```

- Delete a Wishlist - DELETE `/wishlists/<int:wishlist_id>`
```sh
$ curl --location --request DELETE 'localhost:8000/wishlists/6251'

> saim @ Saims-MacBook-Pro.local ~/github/wishlists 18:19:54
$ curl --location --request GET 'localhost:8000/wishlists'
[
  {
    "created_at": "2019-06-06 21:19:42.898070+00:00",
    "id": 6249,
    "items": [
      {
        "category": "recreation",
        "description": "Some description for item # <factory.declarations.Sequence object at 0x7f481ab94fa0>",
        "id": 59,
        "name": "miscellaneous",
        "price": 695.8241679068253,
        "wishlist_id": 6249
      }
    ],
    "last_updated": "2013-05-01 20:29:03.323924+00:00",
    "name": "Wishlist #56",
    "user_id": 593
  },
  {
    "created_at": "2022-10-19 18:10:23.678271+00:00",
    "id": 6250,
    "items": [],
    "last_updated": "2022-10-19 18:10:23.678271+00:00",
    "name": "namesss",
    "user_id": 456
  },
  {
    "created_at": "2022-10-19 18:10:23.678271+00:00",
    "id": 6252,
    "items": [],
    "last_updated": "2022-10-19 18:10:23.678271+00:00",
    "name": "wishlist1",
    "user_id": 456
  }
]
```

- List all Wishlists - GET `/wishlists`
```sh
$ curl --location --request GET 'localhost:8000/wishlists'
[
  {
    "created_at": "2019-06-06 21:19:42.898070+00:00",
    "id": 6249,
    "items": [
      {
        "category": "recreation",
        "description": "Some description for item # <factory.declarations.Sequence object at 0x7f481ab94fa0>",
        "id": 59,
        "name": "miscellaneous",
        "price": 695.8241679068253,
        "wishlist_id": 6249
      }
    ],
    "last_updated": "2013-05-01 20:29:03.323924+00:00",
    "name": "Wishlist #56",
    "user_id": 593
  },
  {
    "created_at": "2022-10-19 18:10:23.678271+00:00",
    "id": 6250,
    "items": [],
    "last_updated": "2022-10-19 18:10:23.678271+00:00",
    "name": "namesss",
    "user_id": 456
  },
  {
    "created_at": "2022-10-19 18:10:23.678271+00:00",
    "id": 6252,
    "items": [],
    "last_updated": "2022-10-19 18:10:23.678271+00:00",
    "name": "wishlist1",
    "user_id": 456
  }
  ]
  ```


- Add an item to a wishlist - POST `/wishlists/<int:wishlist_id>/items`
```sh
$ curl --location --request POST 'localhost:8000/wishlists/6250/items' \
> --header 'Content-Type: application/json' \
> --data-raw '{
>     "name": "Vacuum Cleaner",
>     "id": 789,
>     "wishlist_id": 6250,
>     "category": "Home Appliances",
>     "price": 500.60,
>     "description": "Vacuum Cleaner worth $500!!"
> }'
{
  "category": "Home Appliances",
  "description": "Vacuum Cleaner worth $500!!",
  "id": 789,
  "name": "Vacuum Cleaner",
  "price": 500.6,
  "wishlist_id": 6250
}
```

- Read an item from a Wishlist - GET `/wishlists/<int:wishlist_id>/items/<int:item_id>`
```sh
$ curl --location --request GET 'localhost:8000/wishlists/6250/items/789' \
> --header 'Content-Type: application/json'
{
  "category": "Home Appliances",
  "description": "Vacuum Cleaner worth $500!!",
  "id": 789,
  "name": "Vacuum Cleaner",
  "price": 500.6,
  "wishlist_id": 6250
}
```

- Update an item in a Wishlist - PUT `/wishlists/<int:wishlist_id>/items/<int:item_id>`
```sh
$ curl --location --request GET 'localhost:8000/wishlists/6250/items/789' \
> --header 'Content-Type: application/json'
{
  "category": "Home Appliances",
  "description": "Vacuum Cleaner worth $500!!",
  "id": 789,
  "name": "Vacuum Cleaner",
  "price": 500.6,
  "wishlist_id": 6250
}

$ curl --location --request PUT 'localhost:8000/wishlists/6250/items/789' \
> --header 'Content-Type: application/json' \
> --data-raw '{
>     "name": "Air Conditioner",
>     "id": 789,
>     "wishlist_id": 6250,
>     "category": "Home Appliances",
>     "price": 500.60,
>     "description": "Vacuum Cleaner worth $500!!"
> }'
{
  "category": "Home Appliances",
  "description": "Vacuum Cleaner worth $500!!",
  "id": 789,
  "name": "Air Conditioner",
  "price": 500.6,
  "wishlist_id": 6250
}
```


- List all items in a Wishlist - GET `/wishlists/<int:wishlist_id>/items`
```
$ curl --location --request GET 'localhost:8000/wishlists/6250/items'
[
  {
    "category": "Home Appliances",
    "description": "Vacuum Cleaner worth $500!!",
    "id": 789,
    "name": "Air Conditioner",
    "price": 500.6,
    "wishlist_id": 6250
  }
]
```

- Delete an item in a Wishlist - DELTE `/wishlists/<int:wishlist_id>/items/<int:item_id>`
```sh
$ curl --location --request DELETE 'localhost:8000/wishlists/6250/items/789'
```
