# Restaurant Telegram Bot 🍽️

A feature-rich Telegram bot for restaurant order management, built with Python and the `telebot` library. The bot allows users to browse menus, place orders, track their order history, and process payments.

## Features

### Core Functionality
- 📱 Interactive menu navigation
- 🛒 Order management system
- 💳 Payment processing simulation
- 👤 User account management
- 📊 Order history tracking

### Technical Features
- 🗄️ SQLite database integration
- 🔄 Real-time order updates
- 🎨 Custom keyboard layouts
- 🔒 Session management
- 📦 Modular architecture

## System Requirements

- Python 3.7+
- SQLite3
- Required Python packages:
  - python-telegram-bot
  - python-dotenv
  - sqlite3

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd restaurant-bot
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # For Unix/macOS
.venv\Scripts\activate     # For Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `.venv` directory with your Telegram bot token:
```
TOKEN=your_telegram_bot_token
```

## Project Structure

```
restaurant-bot/
├── tbot.py                 # Main bot file
├── order_manager/         # Order management module
│   ├── __init__.py
│   └── food_order_manager.py
├── db_module/            # Database module
│   ├── __init__.py
│   ├── config.py
│   ├── db_connector.py
│   ├── db_manager.py
│   ├── db_schema.py
│   └── tables.py
├── design/              # UI components
│   ├── __init__.py
│   ├── buttons.py
│   └── menu.py
└── payment/            # Payment processing
    ├── __init__.py
    └── payment_manager.py
```

## Database Schema

The bot uses SQLite with the following main tables:
- `menu_categories`: Stores menu categories
- `menu_items`: Stores individual menu items
- `users`: Stores user information
- `orders`: Stores order details
- `order_items`: Stores items within orders
- `reviews`: Stores user reviews

## Features in Detail

### Menu Navigation
- Hierarchical menu structure
- Category-based item organization
- Interactive item selection
- Quantity selection with custom keyboards

### Order Management
- Real-time order creation and updates
- Multiple items per order
- Order status tracking
- Order history viewing

### Payment Processing
- Animated payment simulation
- Payment status updates
- Order completion confirmation

### User Interface
- Custom keyboard layouts
- Inline keyboards for item selection
- Back navigation support
- Clean chat management

## Usage

1. Start the bot:
```bash
python tbot.py
```

2. In Telegram, search for your bot and start a conversation.

3. Use the following commands:
- `/start`: Initialize or restart the bot
- `Меню`: View the restaurant menu
- `Мои заказы`: View order history
- `Оформить заказ`: Complete current order
- `Почистить чат`: Clear chat history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Authors

[Add author information here]

## Acknowledgments

- Telegram Bot API
- Python telebot library
- SQLite database

