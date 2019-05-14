from pr_details.models import Branch, Tag, Pr
from django.core.management.base import BaseCommand
from django.db import models

class Command(BaseCommand):
    help = 'Displays current time'
    args = 'master'

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)

    def _create_branch(self, branch=None):
        obj, created = Branch.objects.get_or_create(name=branch)
        return

    def handle(self, *args, **kwargs):
        self._create_branch("cdh4")
        br = Branch.objects.get(name=self.branch)
        

        #rr=Branch(name="master2")
        #rr.objects.save()
