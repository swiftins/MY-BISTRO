from .buttons import (create_tile_kbd,
                      create_inline_kbd,
                      create_reply_kbd,
                      create_keyboard_variable_rows
                      )
from .menu import (show_main_menu,
                   show_menu_categories,
                   show_menu_category_items,
                   select_quantity,
                   make_menu_categories,
                   make_menu_category_items,
                   make_quantity_dialog,
                   show_order,
                   show_help,
                   show_feedback
                   )
menu_tree_previous = {
    "Category_menu": ["Main_menu",show_main_menu],
    "Item_menu": ["Category_menu",make_menu_categories],
    "Item_quantity": ["Item_menu",make_menu_category_items],
}