from django.urls import path
from . import views
from .views import PricingListView, PricingCreateView, PricingUpdateView, PricingDeleteView, ProjectDeleteView, update_material

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("register/", views.register, name="register"),
    path("create-quotation/", views.create_project, name="create_quotation"),
    path("project_list/", views.project_list, name="project_list"),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path("projects/<int:project_id>/add_project_element/", views.add_project_element, name="add_project_element",),
    path("projects/<int:project_id>/add_project_material/", views.add_project_material, name="add_project_material",),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("edit_project/<int:project_id>/", views.update_project, name="edit_project"),
    path("admin/projects/remove_element/<int:element_id>/", views.remove_project_element, name="remove_project_element",),
    path("admin/projects/remove_material/<int:material_id>/", views.remove_material, name="remove_material",),
    path("approve-project/<int:project_id>/", views.approve_project, name="approve_project",),
    path('pricings/', PricingListView.as_view(), name='pricing_list'),
    path('pricings/create/', PricingCreateView.as_view(), name='pricing_create'),
    path('pricings/update/<int:pk>/', PricingUpdateView.as_view(), name='pricing_update'),
    path('pricings/delete/<int:pk>/', PricingDeleteView.as_view(), name='pricing_delete'),
    path('projects/<int:project_id>/approve_material/', views.approve_material, name='approve_material'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('update-material/<int:material_id>/', views.update_material, name='update_material'),  # Include your update material pattern
]