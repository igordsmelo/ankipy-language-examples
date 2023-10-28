import time

counter = time.time()


def count(func_took='function took'):
    print(f'{func_took}: {time.time() - counter}')
