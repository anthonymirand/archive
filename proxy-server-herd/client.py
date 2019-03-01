#!/usr/bin/env python

# CS 131 - Twisted Project
# Client Implementation

import logging

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver


class ProxyClientProtocol(LineReceiver):

  def __init__(self, factory):
    self.factory = factory

  def connectionMade(self):
    self.factory.server.connected_servers[
        self.factory.server_name] = self.factory
    logging.info("Connection made from {} to {}".format(
        self.factory.server.server_name, self.factory.server_name))
    self.sendLine(self.factory.data["response"])

  def connectionLost(self, reason):
    # protocol.connectionLost called before factory.clientConnectionLost
    # perhaps due to client disconnecting to server rather than vice-versa
    if self.factory.server_name in self.factory.server.connected_servers:
      del self.factory.server.connected_servers[self.factory.server_name]
      logging.info("Connection lost from {} to {}".format(
          self.factory.server.server_name, self.factory.server_name))


# Modeled from: https://twistedmatrix.com/documents/current/core/howto/clients.html#clientfactory
class ProxyClientFactory(protocol.ClientFactory):

  def __init__(self, server, server_name, data):
    # NOTE: This adds a circular server-client dependency but this isn't an
    #       issue because ProxyClientProtocol disconnects before
    #       ProxyClientFactory
    self.server = server
    self.server_name = server_name
    self.data = data

  def buildProtocol(self, addr):
    self.protocol = ProxyClientProtocol(self)
    return self.protocol

  def sendAT(self, at_message):
    self.protocol.sendLine(at_message)

  def clientConnectionLost(self, connector, reason):
    if self.server_name in self.server.connected_servers:
      del self.server.connected_servers[self.server_name]
      logging.info("Connection lost from {} to {}".format(
          self.server.server_name, self.server_name))

  def clientConnectionFailed(self, connector, reason):
    logging.info("Connection failed from {} to {}".format(
        self.server.server_name, self.server_name))
