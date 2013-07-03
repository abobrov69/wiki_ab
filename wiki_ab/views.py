from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from models import WikiPage
from forms import PageFormEdit

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

class WikiPageMixin (object):
    model = WikiPage
    slug_field = 'pg_url'
    queryset = WikiPage._default_manager.filter (isdeleted=False)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug_field = self.get_slug_field()
        headers = []
        for i in range(0,len(self.kwargs['url'])):
            slug = self.kwargs['url'][i]
            work_queryset = queryset.filter(**{slug_field: slug})
            try:
                obj = work_queryset.get()
#                a = sasl
            except ObjectDoesNotExist:
                raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
            if i == 0:
                if (obj.parent_pg_url):
                    raise Http404('Incorrect url: /{0}/.'.format(slug))
            elif not obj.parent_pg_url or self.kwargs['url'][i-1] != obj.parent_pg_url:
                    raise Http404('Incorrect url: /{0}/.'.format('/'.join(self.kwargs['url'])))
            headers.append(obj.header)
#            elif i != 0:
#                raise Http404('Incorrect url: /{0}/.'.format('/'.join(self.kwargs['url'])))
        self.kwargs['parent_header']= headers[-2] if len(headers)>1 else "Root page"
        if self.show_child:
            work_queryset = queryset.filter(**{'parent_pg_url': obj.pg_url})
            if work_queryset:
                self.kwargs['child']=[]
                for i in work_queryset:
                    self.kwargs['child'].append ({'pg_url':obj.pg_url+'/'+i.pg_url+'/','header':i.header})
        return obj

    def split_url (self):
        self.kwargs['url'] = [v for k,v in self.request.META.items() if k == 'PATH_INFO'][0].split('/')
        if not self.kwargs['url'][-1]: del self.kwargs['url'][-1]
        if not self.kwargs['url'][0]: del self.kwargs['url'][0]

class WikiPageView (WikiPageMixin, DetailView):
    template_name = "wiki_page_detail.html"
    show_child = True

    def dispatch(self, request, *args, **kwargs):
        self.split_url()
        return DetailView.dispatch(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs ['parent'] = '/{0}/'.format('/'.join(self.kwargs['url'][:-1])) if len(self.kwargs['url'])>1 else '/'
        kwargs['parent_header'] = self.kwargs['parent_header']
        kwargs['child'] = self.kwargs.get('child', None)
        return super(WikiPageView,self).get_context_data(**kwargs)

class WikiPageUpdate (WikiPageMixin, UpdateView):
    template_name = "wiki_page_edit.html"
    form_class = PageFormEdit
    show_child = False

    def dispatch(self, request, *args, **kwargs):
        self.split_url()
        del self.kwargs['url'][-1] # exclude /edit
        self.success_url = '/{0}/'.format('/'.join(self.kwargs['url']))
        return UpdateView.dispatch(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs ['parent'] = '/{0}/'.format('/'.join(self.kwargs['url'][:-1])) if len(self.kwargs['url'])>1 else '/'
        kwargs['parent_header'] = self.kwargs['parent_header']
        return super(WikiPageUpdate,self).get_context_data(**kwargs)