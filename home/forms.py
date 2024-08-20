
from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=255, label='Keyword')
    url = forms.URLField(label='URL')
    country = forms.ChoiceField(label='Country', choices=[('co', 'Colombia'),('mx', 'Mexico'), ('us', 'United States'), ('es', 'Spain'),])
    language = forms.ChoiceField(label='Language', choices=[('en', 'English'), ('es', 'Spanish'),])
    email = forms.EmailField(label='Email', required=True)
    accept_terms = forms.BooleanField(label='Aceptar términos y condiciones', required=True)
