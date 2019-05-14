from django.core.management.base import BaseCommand
from django.utils import timezone
import sys
import os
sys.path.append(os.path.join(os.getcwd(),'backend_scripts'))
import utils
import utils1
from utils import ColorPrint as opt



class Command(BaseCommand):
    help = 'Displays current time'

    def success(self,my_sting):
        return self.stdout.write(self.style.SUCCESS(my_sting))
    
    def error(self,my_sting):
        return self.stdout.write(self.style.ERROR(my_sting))

    def warning(self,my_sting):
        return self.stdout.write(self.style.WARNING(my_sting))
    
    def info(self,my_sting):
        return self.stdout.write(self.style.HTTP_INFO(my_sting))

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        opt.p_err("It's now %s" % time)
        opt.p_pass("It's now %s" % time)
        opt.p_warn("%s" % sys.path)
        opt.p_info(os.getcwd())
        (error, out, stderr ) = utils.run('ls -l',cwd='/Users')
        opt.p_info(out)

