from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse
from models import WikiPage

class AboutView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        kwargs ['path'] = [v for k,v in self.request.META.items() if k == 'PATH_INFO'][0]
        return super(AboutView,self).get_context_data(**kwargs)

class RootPageView(TemplateView):
    template_name = "wiki_page_detail.html"
    def get_context_data(self, **kwargs):
        kwargs ['wikipage'] = {'header':'Root page','text':'Root page text'}
        return super(RootPageView,self).get_context_data(**kwargs)

#    def get(self, request, *args, **kwargs):
#        context = self.get_context_data(**kwargs)
#        context['path'] = [v for k,v in request.META.items() if k == 'PATH_INFO'][0]
#        q1 = context.__class__.__name__
#        lkj = self.request
#        q = s
#        return self.render_to_response(context)

def display_meta(request,*kwargs):
    values = request.META.items()
    a = [v for k,v in values if k == 'PATH_INFO'][0]
#    s = q
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

class WikiPageView (DetailView):
    template_name = "wiki_page_detail.html"
    model = WikiPage
    slug_field = 'pg_url'

    def dispatch(self, request, *args, **kwargs):
        url_str = [v for k,v in self.request.META.items() if k == 'PATH_INFO'][0]
        lst = url.split('/')
        if lst[-1]:
            self.kwargs[self.slug_url_kwarg] = lst[-1]
            self.kwargs['parent'] = 1
        else:
            self.kwargs[self.slug_url_kwarg] = lst[-2]
        return super (WikiPageView, self).dispatch(request, *args, **kwargs)
