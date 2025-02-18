from datetime import datetime

def convert_to_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

# Примеры дат
dates = [
    "2023-10-01 12:00:00",
    "2023-10-02 14:30:00",
    "2023-10-03 16:45:00",
]

# Преобразование и вывод
for date in dates:
    converted_date = convert_to_datetime(date)
    print(converted_date)