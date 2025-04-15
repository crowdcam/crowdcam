from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from .models import Organization
from .forms import OrganizationForm, JoinCodeForm
from guardian.shortcuts import assign_perm, get_objects_for_user

def user_has_user_perms(user, org_id):
    org = get_object_or_404(Organization, id=org_id)
    if(not(user.has_perm('user', org))):
        raise PermissionDenied()
    return org

def user_has_admin_perms(user, org_id):
    org = get_object_or_404(Organization, id=org_id)
    if(not(user.has_perm('admin', org))):
        raise PermissionDenied()
    return org

# login_url redirects users to the provided url given they are not logged in
# @login_required is a decorator that says hey this needs login
@login_required()
def create_org(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            # add data from form
            org = form.save(commit=False)
            org.save()

            # create groups for the org
            admin_group = Group.objects.create(name=org.get_admin_group())
            mod_group = Group.objects.create(name=org.get_mod_group())
            user_group = Group.objects.create(name=org.get_user_group())

            assign_perm('user', user_group, org)
            assign_perm('user', mod_group, org)
            assign_perm('user', admin_group, org)
            assign_perm('mod', mod_group, org)
            assign_perm('mod', admin_group, org)
            assign_perm('admin', admin_group, org)
            

            # set the user to be members of these groups
            request.user.groups.add(user_group)
            request.user.groups.add(mod_group)
            request.user.groups.add(admin_group)
            
            # send user to media index page after success
            return redirect('/')
    else:
        form = OrganizationForm()

    return render(request, "organization/create_org.html", {'form': form})

@login_required()
def org_view(request, org_id):
    org = user_has_user_perms(request.user, org_id)
    context = {"org": org}
    return render(request, "organization/org_view.html", context)

@login_required()
def user_orgs(request):

    # get all organizations to filter through
    user_orgs = get_objects_for_user(request.user, 'organization.user')
    context = {"orgs": user_orgs}
    return render(request, "organization/index.html", context)

@login_required()
def admin_index(request, org_id):
    org = user_has_admin_perms(request.user, org_id)
    context = {"org": org}
    return render(request, "organization/admin/index.html", context)

@login_required()
def set_join_code(request, org_id):
    org = user_has_admin_perms(request.user, org_id)

    if request.method == "POST":
        form = JoinCodeForm(request.POST, instance=org)
        if form.is_valid():
            org = form.save(commit=False)
            org.save()
            return redirect('organization:admin_index', org_id=org_id)
    else:
        form = JoinCodeForm(instance=org)
    
    context = {"org": org, "form": form}
    return render(request, "organization/admin/set_join_code.html", context)

@login_required()
def join_org(request):
    pass