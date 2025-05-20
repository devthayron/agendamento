from django.db import models
from django.conf import settings
from django.db.models import Sum

class Agendamento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    cnpj = models.CharField(max_length=18)
    fornecedor = models.CharField(max_length=100)
    email = models.EmailField(max_length=500)
    transportadora = models.CharField(max_length=100)
    nota_fiscal = models.IntegerField()
    pedido = models.CharField(max_length=100)

    GALPAO_CHOICES = [
        ('galpao1', 'galpão1'),
        ('galpao2', 'galpão2'),
        ('galpao3', 'galpão3'),
        ('galpãa4', 'galpão4'),
    ]

    galpao = models.CharField("Galpão", max_length=20,choices=GALPAO_CHOICES,)

    TIPO_CARRO_CHOICES = [
        ('vuc', 'VUC'),
        ('toco', 'Toco'),
        ('truck', 'Truck'),
        ('carreta', 'Carreta'),
    ]

    tipo_carro = models.CharField("Tipo", max_length=20,choices=TIPO_CARRO_CHOICES,)

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('finalizado', 'Finalizado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.data_hora:
            self.data_hora = self.data_hora.date()  # Remove a parte da hora
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fornecedor} - {self.data_hora.strftime('%d/%m/%Y')}"
    
    def cubagem_total(self):
        return self.itens.aggregate(total=Sum('cubagem'))['total'] or 0
    
    def quantidade_total(self):
        return self.itens.aggregate(total=Sum('quantidade'))['total'] or 0

    
class AgendamentoProduto(models.Model):
    agendamento = models.ForeignKey(
        'Agendamento',
        on_delete=models.CASCADE,
        related_name='itens'
    )
    nota_fiscal = models.FloatField("Nota fiscal",default=1)
    mercadoria = models.CharField("Produto", max_length=100)
    quantidade = models.FloatField("Quantidade")
    cubagem = models.FloatField("Cubagem")

    def __str__(self):
        return f"{self.mercadoria} - {self.quantidade} un"
