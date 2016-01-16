#!/usr/bin/python
from threading import Thread
import subprocess
import socket

#ips = {"192.168.1."+str(ip): False for ip in range(1, 100)}

def generate_ips(range_start, range_end):
    return {"192.168.1."+str(ip): False for ip in range(range_start, range_end)}


def ping(ip, ips):
    call = subprocess.Popen(
        ["ping", "-c", "1", ip],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    out, error = call.communicate()
    if not '0 packets received,' in out:
        ips[ip] = True


def print_nice(to_print):
    longest = 0
    for i in to_print:
        if len(i) > longest:
            longest = len(i)
    for i in to_print:
        offset = longest - len(i)
        print i + (" "*offset) + " | " + to_print[i]


def start(ips):
    threads = []
    for ip in ips:
        thread = Thread(target=ping, args=(ip, ips))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return {socket.gethostbyaddr(ip)[0]:ip for ip in ips if ips[ip] == True}

#if __name__ == '__main__':
#    start(generate_ips(1, 100))
