# -*- coding: utf-8 -*-
"""

    Main page views.

"""

__author__ = "Mikko Ohtamaa <mikko@mfabrik.com>"
__copyright__ = "mFabrik Research Oy"
__license__ = "BSD"
__docformat__ = "epytext"

# Python standard library imports
import os
import random
import cgi
import urlparse
import logging

# Appengine imports
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class PigPage(webapp.RequestHandler):
    """ Base class for page renderer """
    

    def render_page(self, template_file_name):
        """ Render a page template from templates folder"""

        
        # Fill in template parameters
        vars = { }
       
        path = os.path.join(os.path.dirname(__file__), 'templates', template_file_name)
        self.response.out.write(template.render(path, vars))

class MainPage(PigPage):
    """ Index page of the site.

    """
    
    def get(self):

        logging.debug("Loading main page")
        self.render_page("main.html")

class InEnglishPage(PigPage):
    """
    """
    def get(self):
        self.render_page("english.html")

class CompaniesPage(PigPage):
    """
    """
    def get(self):
        self.render_page("companies.html")

class BlogsPage(PigPage):
    """
    """
    def get(self):
        self.render_page("blogs.html")


class NotFound(PigPage):
    """
    Handle URIs not found. 
    """
    def get(self):
        self.render_page("404.html")



application = webapp.WSGIApplication([
                                ('/english', InEnglishPage),
                                ('/companies', CompaniesPage),
                                ('/blogs', BlogsPage),
                                ('/', MainPage),                                
                                ('/.*', NotFound),
                            ], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()