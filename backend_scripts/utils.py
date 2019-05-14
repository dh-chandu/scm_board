import subprocess
import os
import shlex
import sys
#from utils1 import ColorPrint as ex

class ColorPrint:

    @staticmethod
    def p_err(message):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + '\n')

    @staticmethod
    def p_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def p_warn(message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def p_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def p_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message + '\x1b[0m' + end)


def run(cmd, cwd='.', verbose=False, shell=False, split = False):
    ex = ColorPrint()
    if verbose is True:
        if cwd is not ".":
            print ("cd %s &&" % cwd)
        print (cmd)

    # Shell commands are parsed by shell as a string
    if not split and not shell:
        cmd = shlex.split(cmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=shell, universal_newlines=True)

    stdout, stderr = map(lambda s: s.rstrip('\n'), p.communicate())
    error = p.wait()

    ex.p_err(stderr)
    return (error, stdout, stderr)
