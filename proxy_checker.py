import os
from threading import Thread
import functools
import time
from subprocess import Popen, PIPE, call
import signal

proxy_list = []


class MyThread(Thread):
    def __init__(self, proxy, maxtime=10):
        self.proxy = proxy.strip()
        self.pipe = None
        self.maxtime = maxtime
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        print '\nproxy ==> %s' % self.proxy
        # self.pipe = Popen(["curl", "-o test.pak http://dl.360safe.com/setup.exe --proxy %s" % self.proxy], shell=True)
        self.pipe = Popen("curl -o test.pak http://dl.360safe.com/setup.exe --proxy %s" % self.proxy, shell=True)
        print 'pid:', self.pipe.pid
        self.pipe.wait()

    def end(self):
        if self.pipe is not None:
            # print 'kill'
            # os.kill(self.pipe.pid, signal.SIGTERM)
            if os.name == 'nt':
                call('taskkill /F /T /PID ' + str(self.pipe.pid), stdout=PIPE, stderr=PIPE)
            else:
                raise Exception('Not support %s' % os.name)
        else:
            # print 'end'
            pass


def use_thread():
    global proxy_list
    for i in proxy_list[:]:
        t = MyThread(i)
        t.start()
        t.join(10)
        t.end()


if __name__ == '__main__':
    with open('proxy.txt') as f:
        proxy_list = f.readlines()
    use_thread()
