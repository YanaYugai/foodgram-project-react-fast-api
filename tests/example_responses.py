users = {
    0: {
        "email": "user@example.com",
        "id": 0,
        "username": "vasya",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": False
    },
    1: {
        "email": "user_1@example.com",
        "id": 1,
        "username": "petya",
        "first_name": "Петя",
        "last_name": "Пупкин",
        "is_subscribed": False
    },
}

recipes = {
    0: {
        "id": 0,
        "tags": [
            {
                "id": 0,
                "name": "Завтрак",
                "color": "#E26C2D",
                "slug": "breakfast"
            }
        ],
        "author": {
            "email": "user@example.com",
            "id": 0,
            "username": "vasya",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": False
            },
            "ingredients": [
                {
                    "id": 0,
                    "name": "Капуста",
                    "measurement_unit": "кг",
                    "amount": 10
                }
            ],
            "is_favorited": True,
            "is_in_shopping_cart": True,
            "name": "string",
            "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
            "text": "string",
            "cooking_time": 1
    },
    1: {
        "id": 1,
        "tags": [
            {
                "id": 1,
                "name": "Обед",
                "color": "#E26C2D",
                "slug": "lunch"
            }
        ],
        "author": {
            "email": "user_1@example.com",
            "id": 0,
            "username": "petya",
            "first_name": "Петя",
            "last_name": "Пупкин",
            "is_subscribed": False
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "Картошка",
                    "measurement_unit": "кг"
                    "amount": 10
                }
            ],
            "is_favorited": True,
            "is_in_shopping_cart": True,
            "name": "string",
            "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
            "text": "string",
            "cooking_time": 1
    },
}

tags = {
    0: {
        "id": 0,
        "name": "Завтрак",
        "color": "#E26C2D",
        "slug": "breakfast"
    },
    1: {
        "id": 1,
        "name": "Обед",
        "color": "#E26C2D",
        "slug": "lunch"
    },
    2: {
        "id": 2,
        "name": "Ужин",
        "color": "#E26C2D",
        "slug": "dinner"
    },
}

ingredients = {
    0: {
        "id": 0,
        "name": "Капуста",
        "measurement_unit": "кг"
    },
    1: {
        "id": 1,
        "name": "Картошка",
        "measurement_unit": "кг"
    },
    2: {
        "id": 2,
        "name": "Морковь",
        "measurement_unit": "кг"
    },
}
