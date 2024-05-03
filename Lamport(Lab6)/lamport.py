from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

class LamportClock:
    def __init__(self, process_id):
        self.process_id = process_id
        self.time = 0

    def increment(self):
        self.time += 1

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1

    def get_time(self):
        return self.time


def local_time(clock):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(clock.get_time(), datetime.now())

def event(pid, clock):
    clock.increment()
    print('Something happened in {} !'.format(pid) + local_time(clock))

def send_message(pipe, pid, clock):
    clock.increment()
    message = ('Empty shell', clock.get_time())
    pipe.send(message)
    print('Message sent from ' + str(pid) + local_time(clock))

def recv_message(pipe, pid, clock):
    message, timestamp = pipe.recv()
    clock.update(timestamp)
    print('Message received at ' + str(pid)  + local_time(clock))

def process_one(pipe12):
    pid = getpid()
    clock = LamportClock(pid)
    event(pid, clock)
    send_message(pipe12, pid, clock)
    event(pid, clock)
    recv_message(pipe12, pid, clock)
    event(pid, clock)

def process_two(pipe21, pipe23):
    pid = getpid()
    clock = LamportClock(pid)
    recv_message(pipe21, pid, clock)
    send_message(pipe21, pid, clock)
    send_message(pipe23, pid, clock)
    recv_message(pipe23, pid, clock)

def process_three(pipe32):
    pid = getpid()
    clock = LamportClock(pid)
    recv_message(pipe32, pid, clock)
    send_message(pipe32, pid, clock)

if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one, args=(oneandtwo,))
    process2 = Process(target=process_two, args=(twoandone, twoandthree))
    process3 = Process(target=process_three, args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
