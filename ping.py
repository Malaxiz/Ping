#!/usr/bin/python
from threading import Thread
import subprocess
import socket

#ips = {"192.168.1."+str(ip): False for ip in range(1, 100)}

def generate_ips(range_start, range_end):
    return {"192.168.1."+str(ip): False for ip in range(range_start, range_end)}


# credit: https://stackoverflow.com/users/416467/kindall
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return


def ping(ip):
    call = subprocess.Popen(
        ["ping", "-c", "1", ip],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    out, error = call.communicate()
    if not '0 packets received,' in out and error == '':
        return True
    return False


def print_nice(to_print):
    longest = 0
    for i in to_print:
        if len(i) > longest:
            longest = len(i)
    for i in to_print:
        offset = longest - len(i)
        print i + (" "*offset) + " | " + to_print[i]


def start(ips):
    threads = {}
    for ip in ips:
        thread = ThreadWithReturnValue(target=ping, args=(ip,))
        thread.start()
        threads[ip] = thread
    for thread in threads:
        ips[thread] = threads[thread].join()
    return {socket.gethostbyaddr(ip)[0]:ip for ip in ips if ips[ip] == True}

#if __name__ == '__main__':
#    start(generate_ips(1, 100))
