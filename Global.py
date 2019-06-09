import threading


class GL:
    SCREEN = (300, 300)
    BUFFER = 1024
    SIZE = int((SCREEN[0] / 2) * (SCREEN[1] / 2) * 3)
    SERVER_FRAME = 0
    CLIENT_FRAME = 0
    COND = threading.Condition()
    STOP = threading.Event()
