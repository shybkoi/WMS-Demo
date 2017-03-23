#!/usr/local/bin/python
# -*- coding: utf-8 -*-

VERSION = '0.1.3'

import argparse
import os
import re
import sys
import urllib2
import subprocess

NGINX_CONF_DEFAULT_PATH = '/usr/local/nginx/conf/nginx.conf'
PING_TIMEOUT = 60 # ms timeout
UPDATER_CRON_TASK = 'cron/devupd'

def importer(location):
    "importing module"
    (head, tail)=os.path.split(location)
    sys.path[0:0] = [head]
    if tail[-3:].lower() == '.py':
        tail = tail[:-3]
    result = __import__(tail)
    del sys.path[0]
    return result

def nginx_port():
    try:
        conf = open(NGINX_CONF_DEFAULT_PATH, 'r')
    except Exception, e:
        "no nginx.conf file"
        return None
    m = re.search(r'^\s*listen\s+(\d+)', conf.read(), re.M)
    if m is not None:
        return m.group(1)
    return None


def ping_localhost(engine_conf, port):
    try:
        if port is None:
            srv_port = engine_conf.socket_port1
        else:
            srv_port = port
        host = "%s://%s:%s" % (engine_conf.server1, engine_conf.socket_host1, srv_port)
        status = urllib2.urlopen(host, timeout=PING_TIMEOUT)
        print status.getcode()
        print status.msg
    except urllib2.URLError, e:
        if hasattr(e, 'code') and hasattr(e, 'msg'):
            print e.code
            print e.msg
        elif port is None:
            print 500
            print "engine is down"
        else:
            print 500
            print "nginx is down"

def ping_server():
    conf_path = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'conf/engine_conf')
    engine_conf = importer(conf_path)
    ping_localhost(engine_conf, nginx_port())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ping', action='store_true')
    parser.add_argument('--newtask')
    args = parser.parse_args()
    ping = args.ping
    newtask = args.newtask
    
    if ping:
        ping_server()
        return
    if newtask:
        pipes = subprocess.Popen("crontab -l", stdout=subprocess.PIPE, shell=True)
        curr_cron = pipes.stdout.read()
        new_cron = ''
        regexp = re.compile(r'^[^#]*%s' % UPDATER_CRON_TASK)
        commented_line = re.compile(r'^\s*#')
        for line in curr_cron.split('\n'):
            if regexp.search(line) is None:
                new_cron += "%s\n" % line
            else:
                new_cron += "%s" % newtask
                
        pipes = subprocess.Popen("crontab", stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pipes.stdin.write(new_cron)
        pipes.stdin.close()
        success = re.compile(r'\S')
        print (lambda err: 'success' if success.search(err) is None else err)(pipes.stderr.read())

if __name__ == '__main__':
    main()

    
