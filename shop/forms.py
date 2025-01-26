from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the name of the product'}),
            'desc':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter the description of the product'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Add image of the product'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the price of the product'}),
            'date_created': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the date created'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the stock of the product'}),
            'available': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of the product'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose category of the product'}),

        }