from django import forms
from .models import Agendamento
from .utils.feriados import get_feriado_nome
import datetime

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = [
            'galpao', 'cnpj', 'fornecedor', 'email', 'transportadora', 'tipo_carro', 
            'pedido', 'nota_fiscal', 'data_hora', 'sem_limite_doca',
        ]
        labels = {
            'data_hora': 'Data', 
        }
        widgets = {
            'data_hora': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}), 
            'transportadora': forms.TextInput(attrs={'class': 'form-control'}),  
            'tipo_carro': forms.Select(attrs={'class': 'form-control'}),  
            'pedido': forms.TextInput(attrs={'class': 'form-control'}),  
            'nota_fiscal': forms.TextInput(attrs={'class': 'form-control'}),  
            'galpao': forms.Select(attrs={'class': 'form-control'}),  
            'sem_limite_doca': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hoje = datetime.date.today().isoformat()
        # Reaplica o widget com formato ao campo
        self.fields['data_hora'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': hoje,
                'id': 'id_data_hora'
            },
            format='%Y-%m-%d'
        )

        # Para que o valor seja mostrado corretamente em edições
        if self.instance and self.instance.data_hora:
            self.initial['data_hora'] = self.instance.data_hora.strftime('%Y-%m-%d')

        # Campos opcionais
        self.fields['galpao'].required = False
        self.fields['pedido'].required = False

    def clean_data_hora(self):
        data = self.cleaned_data['data_hora']
        nome_feriado = get_feriado_nome(data)
        if nome_feriado:
            raise forms.ValidationError(f"Não é possível agendar em feriado: {nome_feriado}.")
        return data
