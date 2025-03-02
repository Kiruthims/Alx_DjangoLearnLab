from django import forms

class ExampleForm(forms.Form):
    
    example_field = forms.CharField(label="Example Field", max_length=100)