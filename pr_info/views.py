from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from pr_details.models import Branch, Tag, Pr
# Create your views here.


#------
#@login_required


def info_list_branches(request):
    branches = Branch.objects.all()
    return render(request, 'info_list_branches.html', {'branches' : branches})

def info_branch_list_tags(request, pk):
    #tags = get_object_or_404(Tag, branch_id=pk)
    #tags = Tag.objects.filter(branch_id=pk)
    br_instance = Branch.objects.filter(id = pk )
    pr_objs = Pr.objects.filter(branch__name = br_instance[0].name ).order_by('tag_id')
    prev_tag = ''
    table_bod = ''
    
    for t_obj in pr_objs:
        if prev_tag != t_obj.tag.tag_name:
            r_count = Pr.objects.filter(branch__name = br_instance[0].name, tag__tag_name=t_obj.tag.tag_name).count()
            table_bod += "<tr><td rowspan=%s>%s</td><td>%s</td><td>%s</td></tr>" % ( r_count, t_obj.tag.tag_name, t_obj.pr, t_obj.status )
        else:
            table_bod += "<tr><td>%s</td><td>%s</td></tr>" % (t_obj.pr, t_obj.status)
        prev_tag = t_obj.tag.tag_name
    
    table_body = mark_safe(table_bod)
    return render(request, 'info_branch_list_tags.html', {'pr_objs': pr_objs, 'table_body' : table_body, 'branch' : br_instance[0]})
