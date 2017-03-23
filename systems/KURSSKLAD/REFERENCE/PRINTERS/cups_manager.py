# -*- coding: cp1251 -*-
#!/usr/bin/env python

from subprocess import Popen, PIPE
import re

class CupsManager():
    active = r'active|start|running'
    inactive = r'inactive|stop|waiting'

    def __shell(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        msg = out + err
        status = (lambda x: 'ok' if x == '' else 'error')(err)
        return (status, msg)


    def cups_status(self):
        raw_cmd = self.__shell('service cups status')
        if raw_cmd[0] == 'error':
            return raw_cmd
        if len(re.findall(self.active, raw_cmd[1])) > 0:
            return raw_cmd
        if len(re.findall(self.inactive, raw_cmd[1])) > 0:
            return ('error', raw_cmd[1])


    def cups_start(self):
        raw_cmd = self.__shell('service cups start')
        if raw_cmd[0] == 'error':
            return raw_cmd
        if len(re.findall(self.active, raw_cmd[1])) > 0:
            return raw_cmd
        if len(re.findall(self.inactive, raw_cmd[1])) > 0:
            return ('error', raw_cmd[1])

    def cups_restart(self):
        raw_cmd = self.__shell('service cups restart')
        if raw_cmd[0] == 'error':
            return raw_cmd
        if len(re.findall(self.active, raw_cmd[1])) > 0:
            return raw_cmd
        if len(re.findall(self.inactive, raw_cmd[1])) > 0:
            return ('error', raw_cmd[1])

    def cups_stop(self):
        raw_cmd = self.__shell('service cups stop')
        if raw_cmd[0] == 'error':
            return raw_cmd
        if len(re.findall(self.inactive, raw_cmd[1])) > 0:
            return raw_cmd
        if len(re.findall(self.active, raw_cmd[1])) > 0:
            return ('error', raw_cmd[1])

    # @param destination - printer name
    def get_printer_queue(self, destination=None):
        if destination is not None:
            cmd = 'lpq -P %s' % destination
        else:
            cmd = 'lpq'
        return self.__shell(cmd)

    # @param destination - printer name
    # @return tuple (status like "ok" or "error", ip like "socket://xxx.xxx.xxx.xxx:ppppp" or "cnijnet:/MA-CA-DD-RE-SS-00")
    def get_printer_ip(self, destination):
        cmd = "lpstat -v | grep %s | awk '{ print $4 }'" % destination
        return self.__shell(cmd)

    # depend installed nmap (yast -i nmap)
    # @param String ip, String or Int port
    # @return "ok" if nmap installed and status. Parse in status ignore case "open" | "fitered" | "closed" | "host seems down"
    def check_port(self, ip, port):
        cmd = 'nmap -p%s %s' % (port, ip)
        return self.__shell(cmd)
