from __future__ import absolute_import

import json
import logging
import httplib
import urllib2

import socks
from celery import task

from node.models import Node
from leakdirectory import __version__
from leakdirectory.celery import app

logger = logging.getLogger(__name__)

class SocksiPyConnection(httplib.HTTPConnection):
    def __init__(self, proxytype, proxyaddr, proxyport=None, rdns=True, username=None, password=None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if type(self.timeout) in (int, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

class SocksiPyHandler(urllib2.HTTPHandler, urllib2.HTTPSHandler):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib2.HTTPHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            conn = SocksiPyConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)

@task
def update_node(hidden_service):
    opener = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, "localhost", 9050))
    opener.addheaders = [('User-agent', 'Leak Directory %s' % __version__)]
    r = opener.open(str(hidden_service + '/node'))
    try:
        node = Node.objects.get(address=hidden_service)
    except Node.DoesNotExist: 
        node = Node()
    try:
        node_data = json.loads(r.read())
        node.name = node_data['name']
        node.description = node_data['description']
        node.address = hidden_service
        node.email = node_data['email']
        node.tor2web_admin = node_data['tor2web_admin']
        node.tor2web_receiver = node_data['tor2web_receiver']
        node.tor2web_submission = node_data['tor2web_submission']
        node.tor2web_unauth = node_data['tor2web_unauth']
        node.default_language = node_data['default_language']
        node.languages_enabled = node_data['languages_enabled']
        node.save()
    except:
        logger.error("Failed to parse /node information")
