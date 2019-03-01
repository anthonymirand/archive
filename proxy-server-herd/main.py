#!/usr/bin/env python

# CS 131 - Twisted Project
# Entry point for running servers (and clients)

import conf
from server import ProxyServerFactory

import sys, requests

from twisted.internet import reactor
from twisted.internet.error import CannotListenError


def usage(error=None, name_error=False):
  print "Usage: python main.py [server_name]"
  if error:
    print "ERROR: {}".format(error)
  if name_error:
    print "Valid server names are: {}".format(conf.SERVER_CONFIG.keys())
  exit()


def main():
  if len(sys.argv) != 2:
    usage()

  server_name = sys.argv[1]
  if server_name not in conf.SERVER_CONFIG:
    usage(
        error="{} is not a valid server name".format(server_name),
        name_error=True)

  try:
    factory = ProxyServerFactory(server_name,
                                 conf.SERVER_CONFIG[server_name]["port"])
    reactor.listenTCP(conf.SERVER_CONFIG[server_name]["port"], factory)
    reactor.run()
  except CannotListenError:
    usage(error="Port {} already in use".format(conf.SERVER_CONFIG[server_name]
                                                ["port"]))


if __name__ == '__main__':
  main()
