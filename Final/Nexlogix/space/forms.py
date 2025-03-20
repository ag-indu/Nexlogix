from django import forms

class SpaceOptimizationForm(forms.Form):
    truck_width = forms.IntegerField(label="Truck Width")
    truck_height = forms.IntegerField(label="Truck Height")
    truck_depth = forms.IntegerField(label="Truck Depth")
    num_types = forms.IntegerField(label="Number of Box Types", min_value=1)

    def __init__(self, *args, **kwargs):
        num_types = kwargs.pop('num_types', 1)
        super(SpaceOptimizationForm, self).__init__(*args, **kwargs)

        for i in range(1, num_types + 1):
            self.fields[f'width_{i}'] = forms.IntegerField(label=f"Width of Box Type {i}", min_value=1)
            self.fields[f'height_{i}'] = forms.IntegerField(label=f"Height of Box Type {i}", min_value=1)
            self.fields[f'depth_{i}'] = forms.IntegerField(label=f"Depth of Box Type {i}", min_value=1)
            self.fields[f'count_{i}'] = forms.IntegerField(label=f"Number of Boxes of Type {i}", min_value=1)
