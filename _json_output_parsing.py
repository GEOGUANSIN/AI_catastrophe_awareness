import json
import pandas as pd


def json_validation(json_string_, mode='normal'):
    if mode == 'normal':
        try:
            # json.loads(json_string_)
            eval(json_string_)
            return True
        except Exception as e:
            return False

    if mode == 'number_indexed':
        try:
            data = json.loads(json_string_)
            previous_key = 0
            for key in data.keys():
                if int(key) - previous_key != 1:
                    return False
                previous_key = int(key)
            return True
        except Exception as e:
            return False


class LoopTilJson:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        k = 0
        while k < 10:
            try:
                k += 1
                result = self.func()
                print(f"result:{result}")
                if json_validation(result[0], mode=result[1]):
                    return eval(result[0])
            except Exception as e:
                pass
        return 'ErrorJsonString'


if __name__ == '__main__':
    @LoopTilJson
    def json_string_making(mode='normal'):
        return '{"1": "John", "2": 30, "3": "New York"}', mode
    print(json_string_making())