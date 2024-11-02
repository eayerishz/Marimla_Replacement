from django import forms
from django.contrib.auth.models import User
from .models import Project, Material, Pricing,ProjectElement


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "start_date",
            "end_date",
            "user",
            "status",
        ]  # Changed to snake_case


class ProjectElementForm(forms.ModelForm):
    class Meta:
        model = ProjectElement
        fields = ["project", "name"]
        exclude = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields["project"].initial = project
            self.fields["project"].widget.attrs["readonly"] = True


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude = ["created_at", "updated_at"]


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Project  # Ensure this is the correct model
        fields = [
            "name",
            "start_date",
            "end_date",
        ]  # Update fields based on the actual model

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "location", "start_date", "end_date", "status"]


class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = ['price', 'materials', 'project']  # Include project if superusers can set it
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'materials': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price < 0:
            raise forms.ValidationError('Price must be a positive number.')
        return price

    def __init__(self, *args, **kwargs):
        super(PricingForm, self).__init__(*args, **kwargs)
        self.fields['materials'].queryset = Material.objects.all()  # Populate materials
        self.fields['project'].queryset = Project.objects.all()    # Populate projects if needed