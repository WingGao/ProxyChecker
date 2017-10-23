#!/usr/bin/env python
# coding=utf-8
import os
import urllib2
from threading import Thread
from subprocess import Popen, PIPE, call
import requests
from colorama import Fore, Back, Style
import argparse
import socks
import json
import time
from multiprocessing import Pool

ss_bin = None
server_success = []


class ProxyCheckerSS(Thread):
    def __init__(self, proxy, maxtime=10, ss_port=None, ss_bin=None):
        self.proxy = proxy
        self.pipe = None
        self.maxtime = maxtime
        # self.https = https
        # self.speed = speed
        if ss_port is None:
            self.ss_port = 31000
        else:
            self.ss_port = ss_port
        self.ss_bin = ss_bin
        Thread.__init__(self)
        self.daemon = True

    def get_server(self):
        return self.proxy['server']

    def check(self):
        r = self.run()

        self.end()
        return r

    def run(self):
        print '\nproxy ==> %s' % (Fore.CYAN + self.proxy['server'] + Style.RESET_ALL)
        self.pipe = Popen('%s -s %s -p %s -k %s -l %i -m %s' % (
            self.ss_bin, self.proxy['server'], self.proxy['server_port'], self.proxy['password'], self.ss_port,
            self.proxy['method']), shell=True)
        print 'pid:', self.pipe.pid
        time.sleep(3)
        # opener = urllib2.build_opener(SocksiPyHandler(socks.SOCKS5, "127.0.0.1", self.ss_port))
        try:
            # r = requests.get('https://www.baidu.com', proxies={'http': self.proxy, 'https': self.proxy})
            proxysrt = 'socks5://127.0.0.1:%i' % self.ss_port
            # url ='http://2017.ip138.com/ic.asp'
            # url = 'http://github.com'
            url = 'https://www.baidu.com'
            r = requests.get(url, proxies={'http': proxysrt, 'https': proxysrt}, timeout=30)
            # r.encoding = 'gbk'
            print r.text
            print Fore.GREEN + 'OK %s' % self.get_server() + Style.RESET_ALL

        except Exception, e:
            print Fore.RED + str(e) + Style.RESET_ALL
            # self.pipe.wait()
        self.end()

    def end(self):
        if self.pipe is not None:
            # print 'kill'
            # os.kill(self.pipe.pid, signal.SIGTERM)
            if os.name == 'nt':
                # windows
                call('taskkill /F /T /PID ' + str(self.pipe.pid), stdout=PIPE, stderr=PIPE)
            elif os.name == 'posix':
                # mac
                call('kill %i' % self.pipe.pid, shell=True)
            else:
                raise Exception('Not support %s' % os.name)
        else:
            print 'end'
            pass


def do_pool(proxy):
    if proxy.check():
        return proxy.get_server()
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ss_bin', help='shadowsocks path')
    parser.add_argument('--no_https', help='not check support https', action='store_true')
    parser.add_argument('--no_speed', help='not check speed', action='store_true')
    args = parser.parse_args()

    proxy_list = []
    with open('ss.json') as f:
        conf = json.load(f)
        p = 31000
        for i in conf['configs']:
            proxy = ProxyCheckerSS(i, ss_port=p, ss_bin=args.ss_bin)
            p += 1
            proxy_list.append(proxy)
    ss_bin = args.ss_bin

    # pool = Pool(1)
    # res = pool.map_async(do_pool, proxy_list)
    # print res.get(15)
    for p in proxy_list:
        p.start()

    for p in proxy_list:
        p.join()
        # p.end()
        # p.check()
        # break
