from collections import defaultdict
from multiprocessing import Process, Queue
import os

from service import get_name_and_volatility, print_result, time_track


class TikerParser(Process):

    def __init__(self, file, que, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file
        self.que = que

    def run(self):
        name, volatility = get_name_and_volatility(self.file)
        self.que.put(dict(name=name, volatility=volatility))


@time_track
def main():
    dict_of_tiker = defaultdict(float)
    null_volatility = []
    que = Queue()
    tikes = [TikerParser(os.path.join(p, file), que) for p, d, f in os.walk(r"trades") for file in f]
    for tik in tikes:
        tik.start()
    for tik in tikes:
        tik.join()
    while not que.empty():
        data = que.get()
        if data['volatility']:
            dict_of_tiker[data['name']] = round(data['volatility'], 2)
        else:
            null_volatility.append(data['name'])

    print_result(dict_of_tiker, null_volatility)


if __name__ == '__main__':
    main()
