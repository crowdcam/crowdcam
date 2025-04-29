from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Organization
from .forms import OrganizationForm,JoinCodeSubmit
from guardian.shortcuts import assign_perm, get_objects_for_user
from .utils import user_has_user_perms


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


