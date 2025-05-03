from django import forms
from .models import Agendamento
import datetime

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = [
            'cnpj', 'fornecedor', 'email', 'transportadora', 'tipo_carro', 
            'pedido', 'nota_fiscal', 'data_hora',
        ]
        widgets = {
            'data_hora': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),  # Estilo para o campo de email
            'transportadora': forms.TextInput(attrs={'class': 'form-control'}),  # Estilo para transportadora
            'tipo_carro': forms.TextInput(attrs={'class': 'form-control'}),  # Estilo para tipo de carro
            'pedido': forms.TextInput(attrs={'class': 'form-control'}),  # Estilo para pedido
            'nota_fiscal': forms.TextInput(attrs={'class': 'form-control'}),  # Estilo para nota fiscal
            'produto': forms.TextInput(attrs={'class': 'form-control'}),  # Estilo para produto
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hoje = datetime.date.today().isoformat()
        self.fields['data_hora'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': hoje,  # Impede seleção de datas anteriores
            }
        )