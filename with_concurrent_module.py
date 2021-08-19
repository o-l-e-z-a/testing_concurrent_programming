import os
from collections import defaultdict

from concurrent import futures

from service import get_name_and_volatility, print_result, time_track


@time_track
def main():
    dict_of_tiker = defaultdict(float)
    null_volatility = []
    tikes = [os.path.join(p, file) for p, d, f in os.walk(r"trades") for file in f]
    workers = max(1, len(tikes))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(get_name_and_volatility, tikes)
    for name, volatility in res:
        if volatility:
            dict_of_tiker[name] = round(volatility, 2)
        else:
            null_volatility.append(name)
    print_result(dict_of_tiker, null_volatility)


if __name__ == '__main__':
    main()