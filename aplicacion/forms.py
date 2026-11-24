
from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "cantidad",
            "estado",
        ]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del producto",
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descripción del producto",
            }),
            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }),
            "cantidad": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "1",
            }),
            "estado": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
