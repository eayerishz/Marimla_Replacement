from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuotationForm, ProjectUpdateForm, ProjectElementForm, MaterialForm
from .models import Project, ProjectElement, Material, Pricing
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PricingForm  # Make sure you create a form for Pricing


def is_superuser(user):
    return user.is_superuser

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


from django.shortcuts import get_object_or_404, redirect, render
from .models import Project
from .forms import ProjectUpdateForm

import logging

logger = logging.getLogger(__name__)

@login_required
def project_detail(request, project_id):
    logger.debug(f"Fetching project with ID: {project_id}")
    project = get_object_or_404(Project, id=project_id)
    form = None

    if request.user.is_superuser:
        if request.method == "POST":
            form = ProjectUpdateForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect('project_detail', project_id=project.id)
        else:
            form = ProjectUpdateForm(instance=project)

    return render(request, "project_detail.html", {
        "project": project,
        "form": form,
    })




from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import Material  # Import your Material model

@login_required
def update_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == 'POST':
        try:
            # Fetch and convert the values from the POST request
            material.qty = int(float(request.POST.get('qty', 0)))  # Convert to float first, then to int
            material.unit = request.POST.get('unit')
            material.price_per_qty = float(request.POST.get('price_per_qty', 0))
            material.markup_percentage = float(request.POST.get('markup_percentage', 0))

            # Save the changes to the database
            material.save()

            # Redirect back to the project details
            return redirect('project_detail', project_id=material.element.project.id)

        except ValueError as e:
            return HttpResponse(f"Invalid input: {e}", status=400)  # Handle invalid conversions

    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests





def home(request):
    projects = (
        Project.objects.all()
        if request.user.is_authenticated
        else Project.objects.none()
    )
    return render(request, "quotations/home.html", {"projects": projects})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("project_list")
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "quotations/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


from django.shortcuts import render, redirect
from .models import Project, ProjectElement, Material
from django.urls import reverse
import datetime

@login_required
def create_project(request):
    if request.method == "POST":
        # Extract form data
        project_name = request.POST.get("project_name")
        area_size = request.POST.get("area_size")
        project_element = request.POST.get("projectElement")
        material_name = request.POST.get("material")

        # Create the Project
        project = Project.objects.create(
            name=project_name,
            area_size=area_size,
            status="Pending",
            start_date=datetime.date.today(),
            user=request.user,
        )

        # Create the ProjectElement linked to the project
        element = ProjectElement.objects.create(project=project, name=project_element)

        # Create the Material linked to the element with default values
        Material.objects.create(
            element=element,
            name=material_name,
            qty=10,            # Replace with actual data if available
            unit="pcs",
            price_per_qty=100,  # Example default price
            markup_percentage=10,
        )

        return redirect(reverse('project_list'))  # Redirect to the project list view after creation

    form = QuotationForm()
    return render(request, "create_project.html", {"form": form})


from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Project  # Replace with your model's name if it's different

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'  # Create this template for confirmation
    success_url = reverse_lazy('project_list')  # Redirect to the project list page after deletion


@login_required
def project_list(request):
    if is_superuser(request.user):
        # Admin can see all projects
        projects = {
            "pendings": Project.objects.filter(status="Pending"),
            "approved": Project.objects.filter(status="Approved"),
            "declined": Project.objects.filter(status="Declined"),
            "completed": Project.objects.filter(status="Completed"),
        }
    else:
        # Regular users can only see their own projects
        projects = {
            "pendings": Project.objects.filter(status="Pending", user=request.user),
            "approved": Project.objects.filter(status="Approved", user=request.user),
            "declined": Project.objects.filter(status="Declined", user=request.user),
            "completed": Project.objects.filter(status="Completed", user=request.user),
        }
    return render(request, "project_list.html", {"projects": projects})


def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = "Approved"
    project.save()
    return redirect("project_list")


def admin_dashboard(request):
    pending_projects = Project.objects.filter(status="Pending")
    approved_projects = Project.objects.filter(status="Approved")
    declined_projects = Project.objects.filter(status="Declined")
    completed_projects = Project.objects.filter(status="Completed")

    return render(
        request,
        "admin_dashboard.html",
        {
            "pending_projects": pending_projects,
            "approved_projects": approved_projects,
            "declined_projects": declined_projects,
            "completed_projects": completed_projects,
        },
    )

from django.shortcuts import redirect, render, get_object_or_404
from .models import Project, ProjectElement, Material
from .forms import ProjectElementForm, MaterialForm


def add_project_element(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = ProjectElementForm(request.POST, project=project)
        if form.is_valid():
            form.save()  # This will save the element and link it to the project
            return redirect('project_detail', project_id=project_id)
    else:
        form = ProjectElementForm(project=project)

    return render(
        request, "add_project_element.html", {"project": project, "form": form}
    )

def add_project_material(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.project = project
            material.save()
            return redirect('project_detail', project_id=project.id)  # Redirect to project details
    else:
        form = MaterialForm()

    return render(
        request, "add_project_material.html", {"project": project, "form": form}
    )



@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.name = request.POST.get("name", project.name)
        project.status = request.POST.get("status", project.status)
        project.save()
        return redirect("project_list")

    project_elements = ProjectElement.objects.filter(project=project)
    materials = Material.objects.filter(element__project=project)

    return render(
        request,
        "update_project.html",
        {
            "project": project,
            "project_elements": project_elements,
            "materials": materials,
        },
    )

def remove_project_element(request, element_id):
    element = get_object_or_404(ProjectElement, id=element_id)
    element.delete()
    return JsonResponse({"message": "Element removed successfully."})

def remove_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    material.delete()
    return JsonResponse({"message": "Material removed successfully."})

# List all pricing entries (accessible to everyone, but could also be restricted)
class PricingListView(View):
    def get(self, request):
        # If the user is a superuser, show all pricing entries
        if request.user.is_superuser:
            pricings = Pricing.objects.all()
        else:
            # Otherwise, show only approved pricing entries
            pricings = Pricing.objects.filter(is_approved=True)

        return render(request, 'pricing/pricing_list.html', {'pricings': pricings})


# Create a new pricing entry (restricted to superusers)
class PricingCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = PricingForm()
        return render(request, 'pricing/pricing_form.html', {'form': form})

    def post(self, request):
        form = PricingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pricing_list')  # Redirect to the list view after saving
        return render(request, 'pricing/pricing_form.html', {'form': form})


# Update an existing pricing entry (restricted to superusers)
class PricingUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, pk):
        pricing = get_object_or_404(Pricing, pk=pk)
        form = PricingForm(instance=pricing)
        return render(request, 'pricing/pricing_form.html', {'form': form})

    def post(self, request, pk):
        pricing = get_object_or_404(Pricing, pk=pk)
        form = PricingForm(request.POST, instance=pricing)
        if form.is_valid():
            form.save()
            return redirect('pricing_list')  # Redirect to the list view after saving
        return render(request, 'pricing/pricing_form.html', {'form': form})


# Delete a pricing entry (restricted to superusers)
class PricingDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, pk):
        pricing = get_object_or_404(Pricing, pk=pk)
        return render(request, 'pricing/pricing_confirm_delete.html', {'pricing': pricing})

    def post(self, request, pk):
        pricing = get_object_or_404(Pricing, pk=pk)
        pricing.delete()
        return redirect('pricing_list')  # Redirect to the list view after deleting

@login_required
def approve_material(request, project_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        material_id = request.POST.get('material_id')

        # Get the material object
        material = get_object_or_404(Material, id=material_id)

        # Update the material's status based on the action
        if action == 'approve':
            material.status = 'approved'
        elif action == 'decline':
            material.status = 'declined'

        material.save()

    return redirect('project_detail', project_id=project_id)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project


@login_required
def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)


    if  project.user == request.user:
        project.status = "Completed"
        project.save()
        messages.success(request, "Project approved successfully.")
    else:
        messages.warning(request,
                         f"{request.user.username} attempted to approve project {project.id}, but does not have permission.")

    return redirect('project_list')


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project

@login_required
def decline_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)


    if  project.user == request.user:
        project.status = "Declined"
        project.save()
        messages.success(request, "Project declined successfully.")
    else:
        messages.warning(request, "You do not have permission to decline this project.")

    return redirect('project_list')