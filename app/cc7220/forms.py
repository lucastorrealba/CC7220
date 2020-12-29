from django import forms


class SearchByNameForm(forms.Form):
    name = forms.CharField(label='Scientist Name', max_length=100)
    lastName = forms.CharField(label='Last name')
