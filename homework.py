import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)
        print()
        print(f'Произведена операция: {record.comment}, на сумму: {record.amount}, дата: {record.date}')
        print()

    def get_amount_spent(self, days_cnt):
        amount_spent = 0
        past = dt.date.today() - dt.timedelta(days=days_cnt)
        today = dt.date.today()
        for values in self.records:
            if past < values.date <= today:
                amount_spent += values.amount
        return amount_spent

    def get_today_stats(self):
        return self.get_amount_spent(1)

    def get_week_stats(self):
        return self.get_amount_spent(7)

    def get_today_remained(self):
        spent = self.get_today_stats()
        left = self.limit - spent
        return left


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        left = self.get_today_remained()
        if left > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью'
                    f' не более {left} кКал')

        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 77.23
    EURO_RATE = 90.74
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        left = self.get_today_remained()

        if left == 0:
            return 'Денег нет, держись'

        all_currency = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (self.RUB_RATE, 'руб')
        }
        currency_divided = round(abs(left) / all_currency[currency][0], 2)
        currency_name = all_currency[currency][1]
        currency_out = f'{currency_divided} {currency_name}'

        if left < 0:
            return f'Денег нет, держись: твой долг - {currency_out}'

        return f'На сегодня осталось {currency_out}'


if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    # дата в параметрах не указана,
    # так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained('rub'))
    # должно напечататься
    # На сегодня осталось 555 руб
    print(f'За неделю потрачено: {cash_calculator.get_week_stats()} руб')

    caloriescalculator = CaloriesCalculator(3000)
    caloriescalculator.add_record(Record(amount=1186, comment="Кусок тортика. И ещё один."))
    caloriescalculator.add_record(Record(amount=84, comment="Йогурт.", date="23.02.2019"))
    caloriescalculator.add_record(Record(amount=1140, comment="Баночка чипсов."))
    caloriescalculator.add_record(Record(amount=900, comment="Пиво Окское"))
    print(caloriescalculator.get_calories_remained())
