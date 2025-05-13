from django import forms
from .models import Agendamento
import datetime

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = [
            'galpao','cnpj', 'fornecedor', 'email', 'transportadora', 'tipo_carro', 
            'pedido', 'nota_fiscal', 'data_hora',
        ]
        widgets = {
            'data_hora': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}), 
            'transportadora': forms.TextInput(attrs={'class': 'form-control'}),  
            'tipo_carro': forms.Select(attrs={'class': 'form-control'}),  
            'pedido': forms.TextInput(attrs={'class': 'form-control'}),  
            'nota_fiscal': forms.TextInput(attrs={'class': 'form-control'}),  
            'produto': forms.TextInput(attrs={'class': 'form-control'}),  
            'galpao': forms.Select(attrs={'class': 'form-control'}),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hoje = datetime.date.today().isoformat()
        self.fields['data_hora'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': hoje,  # Impede seleção de datas anteriores
                'id': 'id_data_hora'
            }
        )