from django.views.generic import TemplateView, DetailView, ListView
from django.http import HttpResponse
from models import WikiPage

class AboutView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        kwargs ['path'] = [v for k,v in self.request.META.items() if k == 'PATH_INFO'][0]
        return super(AboutView,self).get_context_data(**kwargs)

class RootPageView(ListView):
    model = WikiPage
    queryset = WikiPage._default_manager.filter (isdeleted=False, parent_pg_url='')
    template_name = 'wiki_root.html'
    context_object_name = 'pg_list'

#    def get_queryset (self):
#        queryset = super (RootPageView, self).get_queryset()
#        a = c
#        return queryset

def display_meta(request,*kwargs):
    values = request.META.items()
    a = [v for k,v in values if k == 'PATH_INFO'][0]
#    s = q
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def get_parent_url_string(url_str):
    l = url_str.split('/')
    return '/'.join(l[:-1 if l[-1] else -2])+'/'

def get_parent_url_substring(url_str):
    l = url_str.split('/')
    if not l[-1]: del l[-1]
    return '' if len(l)==1 else l[-2]

def get_self_url_substring(url_str):
    l = url_str.split('/')
    return l[-2] if not l[-1] else l[-1]

class WikiPageView (DetailView):
    template_name = "wiki_page_detail.html"
    model = WikiPage
    slug_field = 'pg_url'

    def dispatch(self, request, *args, **kwargs):
        self.kwargs['url'] = [v for k,v in self.request.META.items() if k == 'PATH_INFO'][0].split('/')
        if not self.kwargs['url'][-1]: del self.kwargs['url'][-1]
        if not self.kwargs['url'][0]: del self.kwargs['url'][0]
        self.kwargs[self.slug_url_kwarg] = self.kwargs['url'][-1]
        self.kwargs['parent'] = self.kwargs['url'][-2] if len(self.kwargs['url'])>1 else ''
        return super (WikiPageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs ['parent'] = self.kwargs['parent']
        return super(WikiPageView,self).get_context_data(**kwargs)