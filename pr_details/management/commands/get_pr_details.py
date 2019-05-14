from django.core.management.base import BaseCommand
from django.utils import timezone
from pr_details.models import Branch, Tag, Pr
import sys
import os
import re
sys.path.append(os.path.join(os.getcwd(),'backend_scripts'))
import utils
from utils import ColorPrint 



class Command(BaseCommand):
    help = 'Displays current time'
    args = 'master'
    

    def add_arguments(self, parser):
        parser.add_argument('-b', '--branch', type=str, help='Provide branch name', default='master')
        parser.add_argument('-c', '--clone_path',type=str, help='Provide path to clone git repo',required=True)
        parser.add_argument('-d', '--dry_run', type=int, help='dry run default it is on', default=1)
        parser.add_argument('-l', '--last-tag', type=str, help='Provide last tag')

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)

        

    def _clone(self, path):
        if os.path.exists(self.clone_path):
            opt.p_warn('Repo already exists!!! re-using it now.')
        else:
            (err, opt,sterr) = utils.run(self.clone_command)

    def _db_create_branch(self, branch=None):
        obj, created = Branch.objects.get_or_create(name=branch)
        return

    def _get_tags(self):
        tags = []
        (err, xtags, stder) = utils.run(self.get_tags_cmd, cwd=self.clone_path)
        ytags = xtags.splitlines()
        #tags = list(filter(lambda x: x != self.db_ltag,ytags))
        tags = [ x for x in ytags if not (self.db_ltag in x) or 'LATEST' not in x]
        if tags:
            if self.dry_run:
                self.opt.p_bold("tags_cmd : %s" % self.get_tags_cmd)
                self.opt.p_pass("tags are:")
                self.opt.p_pass(" \n".join(tags))
            return(tags)
        else:
            self.opt.p_err("tags are upto date!!!")
            self.opt.p_err("exiting now")
            exit(0)            
            
    def _get_commits(self,last_tag=None, current_tag=None):
        pretty_format = "git log --pretty=format:%H --first-parent"
        log_cmd = "%s %s..%s" % (pretty_format, last_tag, current_tag)
        (err, commits, stder) = utils.run(log_cmd, cwd=self.clone_path)
        if self.dry_run:
            self.opt.p_bold(log_cmd)
        return commits.splitlines()

    def _get_commit_details(self, commit=None):
        get_authour_cmd = "git log --format=%ae -1 "+commit
        get_all_cmd = "git show "+commit
        if self.dry_run:
            self.opt.p_bold(get_authour_cmd)
            self.opt.p_bold(get_all_cmd)
        
        (err, author, stder) = utils.run(get_authour_cmd, cwd=self.clone_path) 
        (err, opt, stder) = utils.run(get_all_cmd, cwd=self.clone_path)
        #prs = re.findall('\d+', [ x for x in details if x.startswith('PR')][0])
        #prs = " ".join(re.findall('\d+',str([x for x in opt.splitlines() if 'PR:' in x]))) #returns string
        prs = re.findall('\d+',str([x for x in opt.splitlines() if 'PR:' in x])) #returns list
        #url = [ x for x in l if x.startswith('Change U')][0].split('URL: ')[1]
        #url = " ".join(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@#.&+])+', opt)) #returns string
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@#.&+])+', opt)  #returns list
        return (prs, author, url)

    def _checkout_branch(self):
        self.opt.p_pass(self.checkout_cmd)
        (err, opt, sterr) = utils.run(self.checkout_cmd,cwd=self.clone_path)


    def _get_pr_state(self, pr):
        query_cmd = '/usr/local/bin/query-pr -H gnats -P 1529 --expr \'(Branch == \"%s\")\' --format \'\"%%S::%%S\" Number State\'  %s ' % (self.branch, pr)
        self.opt.p_err(query_cmd)
        (err, opt, sterr) = utils.run(query_cmd, cwd=self.clone_path)
        if opt:
            return opt
        else:
            return pr



    def _update_db(self):
        if not self.dry_run : 
            self._db_create_branch(self.branch)
            br_inst = Branch.objects.get(name = self.branch)
        else:
            self.opt.p_err("Its dry-run!! no DB update")

        #tags = []
        tags = self._get_tags()
        #self.opt.p_warn(tags)
        last_tag = "v/"+self.branch+"/"+self.db_ltag
        self.opt.p_warn(last_tag)
        for tag  in tags:
            self.opt.p_warn("-----%s-----" % tag)
            self.opt.p_warn("----DB update for - %s  started ----" % tag)
            tag_inst = Tag()
            tag_inst.tag_name = tag
            
            if not self.dry_run: 
                tag_inst.branch = br_inst
                tag_inst.save()
                self.opt.p_pass("DB update done for :%s" % tag)
                ref_tag_inst = Tag.objects.get(tag_name = tag)
            else : 
                self.opt.p_err("Its dry-run!! no DB update")
            
            
            
            commits = self._get_commits(last_tag=last_tag, current_tag=tag)
            last_tag = tag
            self.opt.p_warn(tag)

            for comit in commits:
                self.opt.p_pass("---- %s ----" % comit)
                (prs, author, url) = self._get_commit_details(comit)
                self.opt.p_bold(" ".join(prs))
                self.opt.p_bold(author)
                self.opt.p_bold(" ".join(url))

                if prs:
                    for pr in prs:
                        pr_inst = Pr()
                        pr_inst.pr = pr 
                        pr_inst.status = self._get_pr_state(pr)  
                        if not self.dry_run:
                            pr_inst.branch = br_inst
                            pr_inst.tag = ref_tag_inst
                            pr_inst.save()
                            self.opt.p_pass("DB update done for PR : %s" % pr)
                        else:
                            self.opt.p_err("Dry run no DB update for PR: %s - %s" % (pr, pr_inst.status) )
                else : 
                    self.opt.p_err("===NO PR INFO for %s" % comit)
            self.opt.p_warn("----DB update for - %s  end      ----" % tag)

            
    def handle(self, *args, **kwargs):
        self.clone_path = kwargs['clone_path']
        self.branch = kwargs['branch']
        self.dry_run = kwargs['dry_run']
        self.opt = ColorPrint()
        if not kwargs['last_tag'] :
            self.db_ltag = Tag.objects.latest('tag_name')
        else :
            self.db_ltag =  kwargs['last_tag']

        self.checkout_cmd = "git checkout " + self.branch
        self.clone_cmd = "git clone evogit:csets/evo-csets" + self.clone_path
        self.get_tags_cmd = "git tag -l v/"+self.branch+"/* --contains "+self.db_ltag
        self.opt.p_pass("WORKSPACE : %s" % self.clone_path)
        self._checkout_branch()
        self._update_db()
        
