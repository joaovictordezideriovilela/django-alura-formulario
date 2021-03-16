from django import forms
from tempus_dominus.widgets import DatePicker
from datetime import datetime
from passagens.classe_viagem import tipos_de_classe
from passagens.validation import *

class PassagensForms(forms.Form):
    origem = forms.CharField(label='Origem', max_length=200)
    destino = forms.CharField(label='Destino', max_length=200)
    data_ida = forms.DateField(label='Data ida', widget=DatePicker())
    data_volta = forms.DateField(label='Data volta', widget=DatePicker())
    data_pesquisa = forms.DateField(label='Data pesquisa', disabled=True, initial=datetime.today())
    classe_viagem = forms.ChoiceField(label='Classe do vôo', choices=tipos_de_classe)
    informacoes = forms.CharField(
        label='Informações extras',
        max_length=200,
        widget=forms.Textarea(),
        required=False
    )
    email = forms.EmailField(label='E-mail', max_length=200)

    def clean(self):
        origem = self.cleaned_data.get('origem')
        destino = self.cleaned_data.get('destino')
        data_ida = self.cleaned_data.get('data_ida')
        data_volta = self.cleaned_data.get('data_volta')
        data_pesquisa = self.cleaned_data.get('data_pesquisa')
        lista_erros = {}
        origem_destino_iguais(origem, destino, lista_erros)
        campo_tem_algum_numero(origem, 'origem', lista_erros)
        campo_tem_algum_numero(destino, 'destino', lista_erros)
        data_ida_maior_data_volta(data_ida, data_volta, lista_erros)
        data_ida_menor_data_hoje(data_ida, data_pesquisa, lista_erros)
        if lista_erros is not None:
            for erro, mensagem_erro in lista_erros.items():
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data