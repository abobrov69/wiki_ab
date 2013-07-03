from django import forms
from models import WikiPage

class PageFormEdit (forms.ModelForm):
    class Meta:
        model = WikiPage
        exclude = ('pg_url','parent_pg_url','isdeleted')
#        fields = ('text')
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 13, 'class': "span9"}),
        }

class PageFormNew (forms.ModelForm):
    class Meta:
        model = WikiPage
        exclude = ('parent_pg_url','isdeleted')
#        fields = ('text')
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 13, 'class': "span9"}),
        }

