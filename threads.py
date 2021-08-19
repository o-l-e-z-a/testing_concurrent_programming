import os
import threading
from collections import defaultdict


from service import get_name_and_volatility, print_result, time_track

dict_of_tiker = defaultdict(float)
null_volatility = []


class TikerParser(threading.Thread):

    def __init__(self, file, lock=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file
        self.lock = lock

    def run(self):
        name, volatility = get_name_and_volatility(self.file)
        if volatility:
            dict_of_tiker[name] = round(volatility, 2)
        else:
            null_volatility.append(name)


@time_track
def main():
    tikes = [TikerParser(os.path.join(p, file)) for p, d, f in os.walk(r"trades") for file in f]
    for tik in tikes:
        tik.start()
    for tik in tikes:
        tik.join()
    print_result(dict_of_tiker, null_volatility)


if __name__ == '__main__':
    main()

