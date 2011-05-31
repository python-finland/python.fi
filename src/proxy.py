# http://gregdoesit.com/2010/12/using-google-app-engine-as-proxy-for-cross-domain-requests/

import logging
import pickle
import urllib
import re
import time
import urllib
import wsgiref.handlers
import hashlib
 
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.runtime import apiproxy_errors
 
CACHE_TIME = 1 # number of minutes to cache content for
 
URL_PREFIXES = ["http://sites.google.com/a/python.fi"] # only allow URLs to be queried from certain domain(s)
 
def getMemcacheKey(url):
  url_hash = hashlib.sha256()
  url_hash.update(url)
  return "hash_" + url_hash.hexdigest()
 
class ProxyHandler(webapp.RequestHandler):
    
    def get(self):
      url = self.request.get('url')
      url = urllib.unquote(url)
      # only allow urls that start with prefixes defined in URL_PREFIXES to be used
      if not self.isUrlAllowed(url):
        self.response.out.write("The URL passed can not be proxied due to security reasons.")
        return
      memcacheKey = getMemcacheKey(url) 
    
      # Use memcache to store the request for CACHE_TIME
      proxiedContent = memcache.get(memcacheKey)
      proxiedContentInMemcache = True
      if proxiedContent is None:
        proxiedContentInMemcache = False
        try:
          response = urlfetch.fetch(url)
        except (urlfetch.Error, apiproxy_errors.Error):
          return self.error(404)
        proxiedContent = response.content
      if proxiedContent is None:
        return self.error(404)
    
      # Add the fetched content to memcache
      if (not proxiedContentInMemcache):
        memcache.add(memcacheKey,proxiedContent,CACHE_TIME)
      self.response.out.write(proxiedContent)

    def isUrlAllowed(self, url):
      for urlPrefix in URL_PREFIXES:
        if url.startswith(urlPrefix):
          return True
      return False
 
app = webapp.WSGIApplication([
  ("/proxy", ProxyHandler),
], debug=True)
 
def main():
  wsgiref.handlers.CGIHandler().run(app)
 
if __name__ == "__main__":
  main()