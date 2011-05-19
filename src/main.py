# -*- coding: utf-8 -*-
"""
    Main page views.
"""

__author__ = "Python Finland <hallitus@python.fi>"
__copyright__ = "Copyright (c) 2011 Python Suomi ry"
__license__ = "BSD"
__docformat__ = "epytext"

# Python standard library imports
import os
import logging

# Appengine imports
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class PigPage(webapp.RequestHandler):
    """Base class for page renderer"""

    def render_page(self, template_file_name):
        """ Render a page template from templates folder"""

        # Fill in template parameters
        vars = {}

        path = os.path.join(os.path.dirname(__file__), 'templates', template_file_name)
        self.response.out.write(template.render(path, vars))


class MainPage(PigPage):
    """Index page of the site"""

    def get(self):
        self.render_page("main.html")


class AboutPage(PigPage):
    def get(self):
        self.render_page("about.html")


class InEnglishPage(PigPage):
    def get(self):
        self.render_page("english.html")


class CompaniesPage(PigPage):
    def get(self):
        self.render_page("companies.html")


class BlogsPage(PigPage):
    def get(self):
        self.render_page("blogs.html")


class JobsPage(PigPage):
    def get(self):
        self.render_page("jobs.html")


class LearnPage(PigPage):
    def get(self):
        self.render_page("learn.html")


class NotFound(PigPage):
    """Handle URIs not found"""
    def get(self):
        self.render_page("404.html")


application = webapp.WSGIApplication([
    ('/about', AboutPage),
    ('/english', InEnglishPage),
    ('/companies', CompaniesPage),
    ('/blogs', BlogsPage),
    ('/jobs', JobsPage),
    ('/learn', LearnPage),
    ('/', MainPage),
    ('/.*', NotFound),
], debug=True)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
