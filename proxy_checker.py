import os
from threading import Thread
import functools
import time
from subprocess import Popen, PIPE, call
import signal

proxy_list = [
    "http://120.24.87.117:81", "http://124.88.67.32:81", "http://124.88.67.10:843", "http://124.88.67.32:83",
    "http://124.88.67.10:83", "http://124.88.67.16:80", "http://121.18.84.4:8998", "http://124.88.67.17:82",
    "http://121.193.143.249:80", "http://125.65.107.57:8081", "http://124.88.67.17:81", "http://124.88.67.23:843",
    "http://124.88.67.21:843", "http://124.88.67.17:80", "http://124.88.67.17:843", "http://203.195.204.168:8080",
    "http://183.59.159.178:8081", "http://124.88.67.17:83", "http://120.27.113.72:8888", "http://116.204.1.111:8081",
    "http://122.142.77.84:81", "http://218.109.127.137:8888", "http://120.25.166.134:3128", "http://119.36.80.104:9999",
    "http://58.53.214.75:8081", "http://124.88.67.39:843", "http://120.27.49.85:8090", "http://124.88.67.10:81",
    "http://121.196.226.246:84", "http://124.88.67.39:80", "http://14.152.93.79:8080", "http://219.82.68.148:8888",
    "http://101.4.136.34:81", "http://180.76.154.5:8888", "http://123.57.184.70:8081", "http://117.21.234.96:8080",
    "http://125.88.74.122:84", "http://125.88.74.122:85", "http://125.88.74.122:82", "http://125.88.74.122:83",
    "http://171.8.79.143:8080", "http://112.17.14.47:80", "http://112.17.14.47:8080", "http://111.13.7.42:81",
    "http://111.13.7.42:82", "http://111.13.7.42:80", "http://58.221.38.170:8080", "http://221.226.82.130:8998",
    "http://59.56.253.58:8081", "http://114.215.153.151:8080", "http://210.13.89.158:8000", "http://183.95.80.165:8080",
    "http://122.227.246.102:808", "http://218.30.114.121:8080", "http://61.182.253.72:8081",
    "http://122.142.77.84:9999", "http://61.166.151.82:8080", "http://112.87.43.47:8081", "http://122.142.77.84:80",
    "http://122.142.77.84:82", "http://60.209.90.211:8888", "http://112.91.135.115:8080", "http://124.88.67.32:80",
    "http://124.88.67.14:843", "http://122.142.77.84:8080", "http://124.166.234.13:9999", "http://124.88.67.24:843",
    "http://124.88.67.14:80", "http://124.88.67.32:843", "http://124.88.67.16:843",
]


class MyThread(Thread):
    def __init__(self, proxy, maxtime=10):
        self.proxy = proxy
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
            # print 'end'
            pass


def use_thread():
    for i in proxy_list[:]:
        t = MyThread(i)
        t.start()
        t.join(10)
        t.end()


if __name__ == '__main__':
    use_thread()
