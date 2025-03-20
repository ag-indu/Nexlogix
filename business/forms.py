from django import forms
from django.contrib.auth.models import User
from .models import Business  # Import your model

class BusinessRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Business
        fields = ['name']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        business = super().save(commit=False)
        business.owner = user
        if commit:
            business.save()
        return business

class TruckPackingForm(forms.Form):
    truck_width = forms.IntegerField(min_value=1, label="Truck Width")
    truck_height = forms.IntegerField(min_value=1, label="Truck Height")
    truck_depth = forms.IntegerField(min_value=1, label="Truck Depth")
    num_box_types = forms.IntegerField(min_value=1, label="Number of Box Types")
