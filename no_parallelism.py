import os
from collections import defaultdict

from service import time_track, get_name_and_volatility, print_result


class TikerParser:

    def __init__(self):
        self.dict_of_tiker = defaultdict(float)
        self.null_volatility = []

    def run(self):
        for p, d, f in os.walk(r"trades"):
            for file in f:
                name, volatility = get_name_and_volatility(os.path.join(p, file))
                if volatility:
                    self.dict_of_tiker[name] = round(volatility, 2)
                else:
                    self.null_volatility.append(name)

    def print(self):
        print_result(self.dict_of_tiker, self.null_volatility)


@time_track
def main():
    tik = TikerParser()
    tik.run()
    tik.print()
    print(len(tik.dict_of_tiker) + len(tik.null_volatility))


if __name__ == '__main__':
    main()
