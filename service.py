import asyncio
import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result
    return surrogate


def get_name_and_volatility(file):
    prices = []
    time.sleep(0.1)
    with open(file, mode='r', encoding='utf8') as f:
        name = file[7:-4]
        for line in f:
            if line[:-1] == 'SECID,TRADETIME,PRICE,QUANTITY':
                continue
            split = line.split(',')
            prices.append(float(split[2]))
    average_price = (max(prices) + min(prices)) / 2
    volatility = (max(prices) - min(prices)) / average_price * 100
    return name, volatility


async def async_get_name_and_volatility(file):
    prices = []
    await asyncio.sleep(0.1)
    with open(file, mode='r', encoding='utf8') as f:
        name = file[7:-4]
        for line in f:
            if line[:-1] == 'SECID,TRADETIME,PRICE,QUANTITY':
                continue
            split = line.split(',')
            prices.append(float(split[2]))
    average_price = (max(prices) + min(prices)) / 2
    volatility = (max(prices) - min(prices)) / average_price * 100
    return name, volatility


def print_result(dict_of_tiker, null_volatility):
    sorted_list = [(name, volatility) for name, volatility in dict_of_tiker.items()]
    sorted_list.sort(key=lambda x: x[1])
    print('Минимальная волатильность:')
    for i in sorted_list[:3]:
        print(f'{i[0]} - {i[1]} %')
    print('Максимальная волатильность:')
    for i in sorted_list[-3:]:
        print(f'{i[0]} - {i[1]} %')
    print('Нулевая волатильность:')
    for i in sorted(null_volatility):
        print(i, end=' ')
    print()
    print(len(sorted_list)+len(null_volatility))
