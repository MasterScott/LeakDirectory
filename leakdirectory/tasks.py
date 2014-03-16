from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import socks
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 9050)
import urllib2
socks.wrapmodule(urllib2)

from leakdirectory.node.models import Node
from leakdirectory import __version__
from leakdirectory.celery import app

@app.task
def update_node(hidden_service):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Leak Directory %s' % __version__)]
    r = opener.open(hidden_service + '/node')
    try:
        node_data = json.loads(r.read())
        node = Node()
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
    except:
        logger.error("Failed to parse /node information")