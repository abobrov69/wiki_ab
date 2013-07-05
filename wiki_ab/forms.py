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
    def __init__(self,**kwargs):
        self.parent_pg_url = kwargs.pop('parent_pg_url',None)
        self.queryset = kwargs.pop ('queryset',None)
        return super(PageFormNew,self).__init__(**kwargs)

    def clean_pg_url(self):
        pg_url = self.cleaned_data['pg_url']
        if self.queryset:
            if self.parent_pg_url:
                work_queryset = self.queryset.filter(**{'parent_pg_url': self.parent_pg_url,"pg_url":pg_url})
                if work_queryset:
                    raise forms.ValidationError("Page {0} already has the child page {1}".format(self.parent_pg_url, pg_url))
            else:
                work_queryset = self.queryset.filter(**{'parent_pg_url': "","pg_url":pg_url})
                if work_queryset:
                    raise forms.ValidationError("Root page already has the child page {0}".format(pg_url))
        return pg_url

    class Meta:
        model = WikiPage
        exclude = ('parent_pg_url','isdeleted')
#        fields = ('text')
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 13, 'class': "span9"}),
        }

