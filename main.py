import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import re
from lib import *
from lib.model import *
from lib.sessutils import *

DOMAIN_NAME = "panjang.in"

_nlstripper_c = re.compile(r"\n|\r|\s\s\s+|\t")

class MainPage(webapp.RequestHandler):
    
    def get(self):
        
        self.sess = get_cookie()
        pj_session = self.sess.get('pj_session')
        
        if pj_session is None:
            # newcomer set session
            self.sess['pj_session'] = get_new_session(self.request.remote_addr,self.request.user_agent)
        
        #self.response.out.write( "pj_session: %s" % self.sess['pj_session'] )
        
        ps = get_pjsession_obj(pj_session)
        user_urls = ps.urls
        
        
        self.response.out.write(
            _nlstripper_c.sub("",
            template.render("template/main.html",{'user_urls':user_urls})
            )
        )
        
    def post(self):
        
        reqget = self.request.get
        self.sess = get_cookie()
        
        orig_url = reqget('url')
        rvf = 'json'
        
        if not valid_url( orig_url ):
            return self.response.out.write(
                return_data(rvf,error = "Invalid url")
            )
            
        if ori_url_exists( orig_url ):
            rec = get_urlrec( orig_url )
            if rec:
                return self.response.out.write(
                    return_data(rvf,
                                exists = 1,
                                code = rec.code,
                                orig_url = rec.orig_url,
                                gen_url = format_url(DOMAIN_NAME, rec.code)
                                )
                )
        
        code = None
        gen_url = None
        while True:
            code, gen_url = generate_short_url(DOMAIN_NAME)
            
            # cari ampe gak ada yg nyamain
            if get_urlrec( code = code ) is None:
                break
        
        if not gen_url:
            return self.response.out.write(
                return_data(rvf,error = "Generation failed")
            )
        
        gen_url = format_url(DOMAIN_NAME, code)
        add_url( self.sess['pj_session'], orig_url, gen_url, code )
        
        return self.response.out.write(
            return_data(rvf,
                        code = code,
                        orig_url = orig_url,
                        gen_url = gen_url
                        )
        )

class UrlRedirector(webapp.RequestHandler):
    
    def get(self,code):
        
        rec = get_urlrec( code = code )
        
        if not rec:
            return self.response.out.write(
                "Url not found"
            )
        
        # add hit counter
        
        hit_url( code, self.request.referer, self.request.user_agent )
        
        return self.redirect(rec.orig_url,permanent=True)
        
        #return self.response.out.write(
        #    "goto: " + rec.orig_url
        #)

class Statistic(webapp.RequestHandler):
    
    def get(self):
        
        code = self.request.get('id')
        
        rec = get_urlrec(code = code)
        
        if not rec:
            return self.response.out.write(return_data('json',error="invalid url"))
            
        lilist = ["<li>%s using `%s`.</li>" % (x.url_referer and "from `%s`" % x.url_referer or "Direct",x.agent) for x in rec.hits]
        if len(lilist) > 0:
            stats = "<ul>%s</ul>" % '\n'.join(lilist)
        else:
            stats = ""
        return self.response.out.write(return_data('json',code=code,stats=str(stats)))
    
    

app = webapp.WSGIApplication(
    [
        ('/api',MainPage),
        ('/',MainPage),
        ('/stat',Statistic),
        ('/(.*)',UrlRedirector),
    ]
)


if __name__ == '__main__':
    run_wsgi_app(app)
