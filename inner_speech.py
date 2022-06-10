import time

class inner_speech():
    def __init__(self):
        a = 0
        while True:
            b = time.time()
            if b - a > 5:
                print("Cada cinco segundos.")
                a = b