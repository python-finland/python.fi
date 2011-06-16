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

from proxy import ProxyHandler

if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
    BASE_URL = 'http://localhost:8080/'
else:
    BASE_URL = 'http://python.fi/'


class SimplePage(webapp.RequestHandler):
    def get(self):
        templatedir = os.path.join(os.path.dirname(__file__), 'templates')

        path = self.request.path.lstrip('/')
        if '..' in path:
            # Prevent possible directory climbing
            path = '_404'
        elif path == '':
            path += 'index'
        elif not path.endswith('/'):
            self.redirect(BASE_URL + path + '/')
            return
        else:
            head, tail = os.path.split(path)
            if tail.startswith('_'):
                path = '_404'

        path = path.rstrip('/')

        if not os.path.isfile(os.path.join(templatedir, path + '.html')):
            if os.path.isfile(os.path.join(templatedir, path, 'index.html')):
                path += '/index'

        path += '.html'

        if not os.path.isfile(os.path.join(templatedir, path)):
            path = '_404.html'

        self.response.out.write(template.render(
            os.path.join(templatedir, path),
            {}
        ))


application = webapp.WSGIApplication([
    ('/proxy', ProxyHandler),
    ('/.*', SimplePage),
], debug=True)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
