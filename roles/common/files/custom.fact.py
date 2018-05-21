#!/usr/bin/env python
import json
import socket
factDictionary = { 'fqdn': socket.getfqdn() }
print json.dumps(factDictionary)
