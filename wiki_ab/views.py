from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView, CreateView
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from models import WikiPage
from gns_string_func import transliterate_and_convert_to_url
from forms import PageFormEdit, PageFormNew
from django.views.decorators.csrf import requires_csrf_token
from django.template import (RequestContext,
                             loader, Template, TemplateDoesNotExist)
from wiki_decode import WikiToHTMLDecoder

@requires_csrf_token
def wiki_page_not_found(request, template_name='404.html', *args, **kwargs):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        template = Template(
            '<h1>Not Found</h1>'
            '<p>The requested URL {{ request_path }} was not found on this server.</p>')
    return HttpResponseNotFound(template.render(RequestContext(request, {'request_path': request.path, 'add_url':get_parent_url_string(request.path)+'add/'})))

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

def display_meta(request,*kwargs):
    values = request.META.items()
    a = [v for k,v in values if k == 'PATH_INFO'][0]
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def get_parent_url_string(url_str):
    l = url_str.split('/')
    if not l[-1]: del l[-1]
    if not l[0]: del l[0]
    return '/{0}/'.format('/'.join(l)) if len (l)>1 else '/'

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
    get_object_return_none = False
    decode_text = False

    def split_url (self):
        self.kwargs['url'] = [v for k,v in self.request.META.items() if k == 'PATH_INFO'][0].split('/')
        if not self.kwargs['url'][-1]: del self.kwargs['url'][-1]
        if not self.kwargs['url'][0]: del self.kwargs['url'][0]

    def get_context_data(self, **kwargs):
        kwargs['parent'] = u'/{0}/'.format(u'/'.join(self.kwargs['url'][:-1])) if len(self.kwargs['url'])>1 else '/'
        kwargs['parent_header'] = self.kwargs.get('parent_header', None)
        kwargs['self_header'] = self.kwargs.get('self_header', None)
        kwargs['child'] = self.kwargs.get('child', None)
        kwargs['self_url'] = self.kwargs['url'][-1]+'/' if self.kwargs['url'] else ''
        kwargs['add_mode'] = self.get_object_return_none
        if self.decode_text:
            kwargs['decoding_text'] = WikiToHTMLDecoder (self.object.text,self.queryset).run_decode()
        return self.upper_class.get_context_data(self,**kwargs)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug_field = self.get_slug_field()
        headers = []
        for i in range(0,len(self.kwargs['url'])):
            slug = self.kwargs['url'][i]
            work_queryset = queryset.filter(**{slug_field: slug})
            try:
                obj = work_queryset.get()
            except ObjectDoesNotExist:
                raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
            if i == 0:
                if (obj.parent_pg_url):
                    raise Http404(u'Incorrect url: /{0}/.'.format(slug)+'<br><a href="/add">Create page</a>' )
            elif not obj.parent_pg_url or self.kwargs['url'][i-1] != obj.parent_pg_url:
                    raise Http404(u'Incorrect url: /{0}/.'.format('/'.join(self.kwargs['url'])))
            headers.append(obj.header)
        self.kwargs['parent_header']= headers[-2] if len(headers)>1 else "Root page"
        self.kwargs['self_header']= headers[-1] if len(headers)>0 else "Root page"
        if self.show_child:
            work_queryset = queryset.filter(**{'parent_pg_url': obj.pg_url})
            if work_queryset:
                self.kwargs['child']=[]
                for i in work_queryset:
                    self.kwargs['child'].append ({'pg_url':obj.pg_url+'/'+i.pg_url+'/','header':i.header})
        return obj if not self.get_object_return_none else None

class WikiPageView (WikiPageMixin, DetailView):
    template_name = "wiki_page_detail.html"
    show_child = True
    upper_class = DetailView
    decode_text = True

    def dispatch(self, request, *args, **kwargs):
        self.split_url()
        return DetailView.dispatch(self, request, *args, **kwargs)

class WikiPageUpdate (WikiPageMixin, UpdateView):
    template_name = "wiki_page_edit.html"
    form_class = PageFormEdit
    upper_class = UpdateView
    show_child = False

    def dispatch(self, request, *args, **kwargs):
        self.split_url()
        del self.kwargs['url'][-1] # exclude /edit
        self.success_url = u'/{0}/'.format('/'.join(self.kwargs['url']))
        return UpdateView.dispatch(self, request, *args, **kwargs)

class WikiPageDelete(WikiPageMixin,DeleteView):
    template_name = "wiki_page_confirm_delete.html"
    upper_class = DeleteView
    show_child = False

    def dispatch(self, request, *args, **kwargs):
        self.split_url()
        del self.kwargs['url'][-1] # exclude /delete
        self.success_url = u'/{0}/'.format('/'.join(self.kwargs['url'][:-1])) if len(self.kwargs['url'])>1 else '/'
        return DeleteView.dispatch(self, request, *args, **kwargs)

class WikiPageCreate(WikiPageMixin,UpdateView):
    template_name = "wiki_page_edit.html"
    form_class = PageFormNew
    upper_class = UpdateView
    show_child = False
    get_object_return_none = True

    def dispatch(self, request, *args, **kwargs):
        self.split_url()
        del self.kwargs['url'][-1] # exclude /add
        self.parent_pg_url = self.kwargs['url'][-1] if self.kwargs['url'] else ''
        return UpdateView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if not self.object.pg_url:
            self.object.pg_url = transliterate_and_convert_to_url (self.object.header)
        self.object.parent_pg_url = self.parent_pg_url
        self.object.save()
        self.success_url = (u'/{0}/'.format('/'.join(self.kwargs['url'])) if len(self.kwargs['url'])>0 else '/') + self.object.pg_url + '/'
        return super(WikiPageCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(WikiPageCreate,self).get_form_kwargs()
        kwargs['parent_pg_url'] = self.parent_pg_url
        kwargs['queryset'] = self.queryset
        return kwargs


