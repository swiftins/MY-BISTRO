tables = {
    "menu_categories" : "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL ",
    "menu_items" : """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        price NUMERIC NOT NULL,
        FOREIGN KEY (category_id) REFERENCES menu_categories(id)
""",
    "users" : """
        id TEXT PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        username TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """,
    "orders" : """
        id TEXT PRIMARY KEY,
        user_id TEXT,
        status TEXT NOT NULL,
        total_price NUMERIC,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        payed_at TIMESTAMP,
        handed_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    """,
    "order_items" : """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        menu_item_id INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    """,
    "reviews" : """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        menu_item_id INTEGER,
        rating INTEGER NOT NULL,
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    """,
}

# CREATE TABLE IF NOT EXISTS menu_categories (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL
# );


# CREATE TABLE IF NOT EXISTS menu_items (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     category_id INTEGER,
#     name TEXT NOT NULL,
#     description TEXT,
#     price NUMERIC NOT NULL,
#     FOREIGN KEY (category_id) REFERENCES menu_categories(id)
# );


# CREATE TABLE IF NOT EXISTS users (
#     id TEXT PRIMARY KEY,
#     telegram_id INTEGER UNIQUE,
#     username TEXT UNIQUE,
#     first_name TEXT,
#     last_name TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# CREATE TABLE IF NOT EXISTS orders (
#     id TEXT PRIMARY KEY,
#     user_id TEXT,
#     status TEXT NOT NULL,
#     total_price NUMERIC,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );

# CREATE TABLE IF NOT EXISTS order_items (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     order_id TEXT,
#     menu_item_id INTEGER,
#     quantity INTEGER NOT NULL,
#     FOREIGN KEY (order_id) REFERENCES orders(id),
#     FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
# );

# CREATE TABLE IF NOT EXISTS reviews (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id TEXT,
#     menu_item_id INTEGER,
#     rating INTEGER NOT NULL,
#     comment TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id),
#     FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
# );
