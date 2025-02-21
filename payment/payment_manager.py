from telebot.types import Message
import time

from order_manager import init_fo_manager
#from tbot import user_data


def process_payment_animation(bot,message: Message,
                              order_number: str,
                              username: str,
                              amount: float,
                              order_id,
                              user_data):
    """
    Создает и обновляет анимированное сообщение о процессе оплаты
    """
    user_id = message.chat.id

    # Начальное сообщение
    payment_message = bot.send_message(
        message.chat.id,
        f"🔄 *Обработка оплаты*\n\n"
        f"*Заказ:* `{order_number}`\n"
        f"*Покупатель:* {username}\n"
        f"*Сумма:* {amount:,.2f} ₽\n\n"
        f"└── Инициализация платежа...",
        parse_mode='Markdown'
    )

    # Этапы обработки платежа
    stages = [
        ("├── Подключение к платежному шлюзу... ⌛️", 3),
        ("├── Проверка данных... ✨", 3),
        ("├── Обработка транзакции... 💳", 4),
        ("├── Подтверждение платежа... ⚡️", 3),
        ("└── Платёж успешно завершён! ✅", 2)
    ]

    progress_indicators = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    for i, (stage, delay) in enumerate(stages):
        # Анимация загрузки
        for _ in range(int(delay * 2)):  # Количество кадров анимации
            current_stages = [
                f"✅ {stages[j][0]}" if j < i else
                f"{progress_indicators[_ % len(progress_indicators)]} {stages[j][0]}" if j == i else
                f"⭕️ {stages[j][0]}"
                for j in range(len(stages))
            ]

            message_text = (
                f"🔄 *Обработка оплаты*\n\n"
                f"*Заказ:* `{order_number}`\n"
                f"*Покупатель:* {username}\n"
                f"*Сумма:* {amount:,.2f} ₽\n\n"
                f"{chr(10).join(current_stages)}"
            )

            bot.edit_message_text(
                message_text,
                chat_id=payment_message.chat.id,
                message_id=payment_message.message_id,
                parse_mode='Markdown'
            )
            time.sleep(0.5)

    # Финальное сообщение
    final_message = (
        f"✅ *Оплата успешно завершена*\n\n"
        f"*Заказ:* `{order_number}`\n"
        f"*Покупатель:* {username}\n"
        f"*Сумма:* {amount:,.2f} ₽\n\n"
        f"Спасибо за заказ! 🎉"
    )

    bot.edit_message_text(
        final_message,
        chat_id=payment_message.chat.id,
        message_id=payment_message.message_id,
        parse_mode='Markdown'
    )
    food_order_manager = init_fo_manager()
    food_order_manager.update_order_status(order_id,"paid")
    food_order_manager.db_manager.close()
    user_data[user_id]["pay_order"] = None



