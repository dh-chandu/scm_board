import subprocess
import os
import shlex
import sys

class ColorPrint:

    @staticmethod
    def p_err(self, message, end = '\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def p_pass(self, message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def p_warn(self,message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def p_info(self,message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def p_bold(self,message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)
    
    def run(cmd, cwd='.', verbose=False, shell=False, split = False):
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
        print("this is from RUN function")
        self.p_err(stdout)
        print("end RUN opt")
        return (error, stdout, stderr)