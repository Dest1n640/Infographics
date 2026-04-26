import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Настройки
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
num_rows = 1000 # Количество транзакций

categories = {
    'Супермаркеты': 'Списание',
    'Рестораны и кафе': 'Списание',
    'Транспорт': 'Списание',
    'Здоровье и красота': 'Списание',
    'Прочие расходы': 'Списание',
    'Перевод СБП': 'Пополнение',
    'Зарплата': 'Пополнение',
    'Кэшбек': 'Пополнение'
}

data = []

current_balance = 50000.0

for _ in range(num_rows):
    date = start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds())))
    category = np.random.choice(list(categories.keys()))
    t_type = categories[category]
    
    # Сумма транзакции
    if t_type == 'Списание':
        amount = round(np.random.uniform(50, 5000), 2)
        current_balance -= amount
        bonus = f"+{round(amount * 0.01, 2)}" if np.random.rand() > 0.5 else "0" # Кэшбек 1%
    else:
        amount = round(np.random.uniform(1000, 60000), 2)
        current_balance += amount
        bonus = "0"

    data.append([
        date.strftime('%d.%m.%Y'),
        date.strftime('%H:%M'),
        category,
        t_type,
        amount,
        round(current_balance, 2),
        bonus
    ])

df = pd.DataFrame(data, columns=['transactiondate', 'time', 'category', 'type', 'amount', 'balance', 'bonusValue'])
df = df.sort_values(by=['transactiondate']).reset_index(drop=True)
df.to_csv('bank_statement.csv', index=False, sep=';')
print("Файл bank_statement.csv успешно создан!")
