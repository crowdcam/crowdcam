from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .models import Organization
from .forms import OrganizationForm, JoinCodeForm, JoinCodeSubmit, UpdateUser
from guardian.shortcuts import assign_perm, get_objects_for_user, remove_perm
import csv
from io import BytesIO

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
    context = {
        "org": org,             
        "is_user": request.user.has_perm('user', org),
        "is_mod": request.user.has_perm('mod', org),
        "is_admin": request.user.has_perm('admin', org),
    }
    return render(request, "organization/org_view.html", context)

@login_required()
def user_orgs(request):

    # get all organizations to filter through
    user_orgs = get_objects_for_user(request.user, 'organization.user')

    org_permissions = []
    for org in user_orgs:
        org_permissions.append({
            "org": org,
            "is_user": request.user.has_perm('user', org),
            "is_mod": request.user.has_perm('mod', org),
            "is_admin": request.user.has_perm('admin', org),
        })
    context = {
        "orgs": org_permissions
    }
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


            # TODO: Check for duplicate join codes from other orgs
            org_list = Organization.objects.all()
            duplicates = False
            for org in org_list:
                if form.cleaned_data["join_code"] == org.join_code and org.id != org_id:
                    duplicates = True
                    break
            if duplicates:
                context = {"err": "That join code is already in use!", "org": org, "form": form}
                return render(request, "organization/admin/set_join_code.html", context)

            org = form.save(commit=False)
            org.save()
            return redirect('organization:admin_index', org_id=org_id)
    else:
        form = JoinCodeForm(instance=org)
    
    context = {"org": org, "form": form}
    return render(request, "organization/admin/set_join_code.html", context)

@login_required()
def join_org(request):
    if request.method == "POST":
        form = JoinCodeSubmit(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data["input_code"]
            org_list = Organization.objects.all()
            selected_org = None
            for org in org_list:
                if org.accepting_users:
                    if org.join_code == join_code:
                        selected_org = org

            if selected_org is None:
                context = {"form": form, "err": "Invalid Join Code. Either the code was wrong or the org is not accepting new users right now"}
                
                return render(request, "organization/join_org.html", context)

            group = Group.objects.get(name=selected_org.get_user_group())
            request.user.groups.add(group)
            return redirect('organization:org_view', org_id=selected_org.id)
    else:
        form = JoinCodeSubmit()
    
    context = {"form": form}
    return render(request, "organization/join_org.html", context)

@login_required()
def manage_users(request, org_id):
    org = user_has_admin_perms(request.user, org_id)
    group = Group.objects.get(name=org.get_user_group())
    users = group.user_set.all()
    user_permissions = []
    for user in users:
        user_permissions.append({
            "user": user,
            "is_user": user.has_perm('user', org),
            "is_mod": user.has_perm('mod', org),
            "is_admin": user.has_perm('admin', org),
        })
    context = {
        "users": user_permissions, 
        "org_id": org_id, 
    }
    return render(request, "organization/admin/manage_users.html", context)

@login_required()
def manage_user(request, org_id, user_id):
    org = user_has_admin_perms(request.user, org_id)
    user = get_object_or_404(User, id=user_id)
    context = {"org": org, "user": user, "org_id": org_id}
    if request.method == "POST":
        form = UpdateUser(request.POST)

        if (form.is_valid()):

            # get each group and add/remove based on role
            user_group = Group.objects.get(name=org.get_user_group())
            mod_group = Group.objects.get(name=org.get_mod_group())
            admin_group = Group.objects.get(name=org.get_admin_group())

            if(form.cleaned_data["permissions"] == 'admin'):
                user.groups.add(user_group)
                user.groups.add(mod_group)
                user.groups.add(admin_group)
                
            elif(form.cleaned_data["permissions"] == 'mod'):
                user.groups.add(user_group)
                user.groups.add(mod_group)
                user.groups.remove(admin_group)
                
            elif(form.cleaned_data["permissions"] == 'user'):
                user.groups.remove(mod_group)
                user.groups.remove(admin_group)
                user.groups.add(user_group)
                
            elif(form.cleaned_data["permissions"] == 'none'):
                # while removing groups should suffice, this ensures their removal
                user.groups.remove(user_group)
                user.groups.remove(mod_group)
                user.groups.remove(admin_group)
                remove_perm('user', user, org)
                
            context["msg"] = "Updated User!"
        else:
            context["msg"] = "Something went wrong..."
    # get the user by ID

    # find the max perms for a given user
    if user.has_perm('admin', org):
        max_perms = 'admin'
    elif user.has_perm('mod', org):
        max_perms = 'mod'
    elif user.has_perm('user', org):
        max_perms = 'user'
    else:
        max_perms = 'none'
        context["user"] = None
        
    form = UpdateUser(initial={'permissions': max_perms})
    context["form"] = form
    context["perms"] = max_perms
    
    return render(request, "organization/admin/user.html", context)

@login_required()
def download_users(request, org_id):
    org = user_has_admin_perms(request.user, org_id)

    # Find all of the users in the org.get_user_group()
    user_group = Group.objects.get(name=org.get_user_group())
    users = user_group.user_set.all()

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{org.name}-users.csv"'},
    )
    
    # Create a CSV writer
    csv_writer = csv.writer(response)
    csv_writer.writerow(['ID', 'Username', 'User', 'Mod', 'Admin'])

    # Write their id, username, user, mod, admin to the CSV file
    for user in users:
        csv_writer.writerow([
            user.id,
            user.username,
            user.has_perm('user', org),
            user.has_perm('mod', org),
            user.has_perm('admin', org),
        ])

    return response
