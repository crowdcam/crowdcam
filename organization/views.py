from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Organization
from .forms import OrganizationForm



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
            admin_group = Group.objects.create(name=org.name + "_admin")
            mod_group = Group.objects.create(name=org.name + "_mod")
            user_group = Group.objects.create(name=org.name + "_user")

            # grab the content type for the permissions
            content_type = ContentType.objects.get_for_model(Organization)

            # create permissions for each group
            user_perms = Permission.objects.create(
                codename=org.name+"_user",
                name="Member of the organization",
                content_type=content_type
            )
            mod_perms = Permission.objects.create(
                codename=org.name+"_mod",
                name="Moderator of the organization",
                content_type=content_type
            )
            admin_perms = Permission.objects.create(
                codename=org.name+"_admin",
                name="Admin of the organization",
                content_type=content_type
            )

            # Add the permissions to the groups
            user_group.permissions.set([user_perms])
            mod_group.permissions.set([mod_perms, user_perms])
            admin_group.permissions.set([admin_perms, mod_perms, user_perms])
            
            # send user to media index page after success
            return redirect('/')
    else:
        form = OrganizationForm()

    return render(request, "organization/create_org.html", {'form': form})

@login_required
def org_view(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    context = {"org": org}
    return render(request, "organization/org_view.html", context)

@login_required
def user_orgs(request):

    # get all organizations to filter through
    organizations = Organization.objects.all()

    user_orgs = []

    for org in organizations:
        if(request.user.has_perm(org.name + "_user")):
            user_orgs.append(org)
    context = {"orgs": user_orgs}
    return render(request, "organization/index.html", context)