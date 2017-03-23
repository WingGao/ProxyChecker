#!/usr/bin/env python
# coding=utf-8
import os
from threading import Thread
from subprocess import Popen, PIPE, call
import requests
from colorama import Fore, Back, Style
import argparse

proxy_list = []


class MyThread(Thread):
    def __init__(self, proxy, maxtime=10, https=True, speed=True):
        self.proxy = proxy.strip()
        self.pipe = None
        self.maxtime = maxtime
        self.https = https
        self.speed = speed
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        print '\nproxy ==> %s' % (Fore.CYAN + self.proxy)
        # https checker
        if self.https and self.proxy.startswith('http:'):
            httpsproxy = self.proxy.replace('http:', 'https:')
            try:
                r = requests.get('https://www.baidu.com', proxies={'http': self.proxy, 'https': self.proxy})
                r.encoding = 'utf-8'
                if 'www.baidu.com/more' in r.text:
                    print Fore.GREEN + 'support HTTPS'
                else:
                    raise Exception('not support https')
            except:
                print Style.RESET_ALL + 'not support HTTPS'

        print Style.RESET_ALL
        # speed checker
        if self.speed:
            self.pipe = Popen("curl -o test.pak http://dl.360safe.com/setup.exe --proxy %s" % self.proxy, shell=True)
            print 'pid:', self.pipe.pid
            self.pipe.wait()

    def end(self):
        if self.pipe is not None:
            # print 'kill'
            # os.kill(self.pipe.pid, signal.SIGTERM)
            if os.name == 'nt':
                # windows
                call('taskkill /F /T /PID ' + str(self.pipe.pid), stdout=PIPE, stderr=PIPE)
            elif os.name == 'posix':
                # mac
                call('pkill curl', shell=True)
            else:
                raise Exception('Not support %s' % os.name)
        else:
            # print 'end'
            pass


def use_thread(args):
    global proxy_list
    for i in proxy_list[:]:
        t = MyThread(i, https=not args.no_https, speed=not args.no_speed)
        t.start()
        t.join(10)
        t.end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no_https', help='not check support https', action='store_true')
    parser.add_argument('--no_speed', help='not check speed', action='store_true')
    args = parser.parse_args()

    with open('proxy.txt') as f:
        proxy_list = f.readlines()
    use_thread(args)
