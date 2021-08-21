import asyncio
import os
from collections import defaultdict

from service import print_result, time_track, async_get_name_and_volatility


@time_track
def main():
    dict_of_tiker = defaultdict(float)
    null_volatility = []
    tikes = [async_get_name_and_volatility(os.path.join(p, file)) for p, d, f in os.walk(r"trades") for file in f]
    loop = asyncio.get_event_loop()
    wait_coro = asyncio.wait(tikes)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    for i in res:
        name, volatility = i.result()
        if volatility:
            dict_of_tiker[name] = round(volatility, 2)
        else:
            null_volatility.append(name)
    print_result(dict_of_tiker, null_volatility)


if __name__ == '__main__':
    main()
