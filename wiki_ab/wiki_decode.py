# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ObjectDoesNotExist

def check_correct_url(url_str, queryset):
    list_url = url_str.split('/')
    if not list_url[-1]: del list_url[-1]
    if not list_url[0]: del list_url[0]
    for i in range(0,len(list_url)):
        slug = list_url[i]
        work_queryset = queryset.filter(**{'pg_url': slug})
        try:
            obj = work_queryset.get()
        except ObjectDoesNotExist:
            return (u'/add' if i==0 else u'/{0}/'.format('/'.join(list_url[:i]))+'add',False)
        if i == 0:
            if (obj.parent_pg_url):
                return (u'/add',False)
        elif not obj.parent_pg_url or list_url[i-1] != obj.parent_pg_url:
            return (u'/{0}/'.format('/'.join(list_url[:i]))+'add',False)
    return (u'/{0}/'.format(u'/'.join(list_url)) if len (list_url)>0 else '/', obj.header)

class WikiToHTMLDecoder(object):
    wiki_tags_re_str = [r'\*\*', '__', '//', '"' ]
    html_tags_start = ['<b>', '<u>', '<i>', '&laquo;']
    html_tags_end = ['</b>', '</u>', '</i>', '&raquo;']

    def __init__(self, wiki_text, queryset):
        self.wiki_text = wiki_text
        self.queryset = queryset
        self.exp_find_link = re.compile(r'\[\[([^\]]*)\]\]')
        self.wiki_tags_re = [re.compile(x) for x in self.wiki_tags_re_str]

    def replace_one_tag (self, str_in, tag_number):
        positions = [x.span() for x in self.wiki_tags_re[tag_number].finditer(str_in)]
        if not positions: return str_in
        str_res = ('' if positions[0][0] == 0 else str_in[:positions[0][0]])
        n = len(positions)
        for i in range(1,n,2):
            str_res += self.html_tags_start[tag_number] + str_in[positions[i-1][1]:positions[i][0]] + \
                       self.html_tags_end[tag_number] + str_in[positions[i][1]:(len(str_in) if i>=n-1 else positions[i+1][0])]
        str_res += self.html_tags_end[tag_number] + str_in[positions[n-1][1]:] if n % 2 else ''
        return str_res

    def wiki_to_html_decode_without_links (self, str_in):
        for i,h in enumerate(self.html_tags_end):
            str_in = self.replace_one_tag(str_in,i)
        return str_in

    def link_decode (self, str_in):
        s = str_in.strip().split(' ',1)
        href_txt = self.wiki_to_html_decode_without_links(s[1]) if len(s)>1 else None
        href_link = s[0].lower().strip()
        if href_link.startswith('http'):
            return u'<a href="' + href_link +'" target=_blank>' + (href_txt if href_txt else href_link) + u'</a>'
        else:
            href_link = check_correct_url(href_link, self.queryset)
            return u'<a href="' + href_link[0] +u'">' + (href_txt if href_txt else href_link[1]) + u'</a>' if href_link[1] \
                else u'<a href="' + href_link[0] +u'"><font color="red">' + (href_txt if href_txt else u'Некорректный адрес страницы') + u'</font></a>'

    def run_decode(self):
        lst_find_all = self.exp_find_link.findall (self.wiki_text)
        a = self.wiki_text
        if lst_find_all:
            links_iter = iter([self.link_decode(s) for s in lst_find_all])
            res = ''
            str_wo_links = self.wiki_to_html_decode_without_links(u'\u0901'.join([x for x in self.exp_find_link.split(self.wiki_text) if x not in lst_find_all])).split(u'\u0901')
            for i in range(len(str_wo_links)-1):
                n = next(links_iter)
                res += str_wo_links[i] + n
            res += str_wo_links[-1]
        else: res = self.wiki_to_html_decode_without_links(self.wiki_text)
        return res



