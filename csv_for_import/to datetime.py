from datetime import datetime

# Строки с датами и временем
date_strings = [
    "2023-10-01 12:00:00",
    "2023-10-02 14:30:00",
    "2023-10-03 16:45:00"
]

# Преобразование строк в объекты datetime
date_objects = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") for date_str in date_strings]

# Вывод объектов datetime
for date in date_objects:
    print(date)