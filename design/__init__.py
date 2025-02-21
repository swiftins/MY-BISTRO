from .buttons import (create_tile_kbd,
                      create_inline_kbd,
                      create_reply_kbd,
                      create_keyboard_variable_rows
                      )
from .menu import *

menu_tree_previous = {
    "Category_menu": ["Main_menu",show_main_menu],
    "Item_menu": ["Category_menu",make_menu_categories],
    "Item_quantity": ["Item_menu",make_menu_category_items],
}