#!/usr/bin/env python

# CS 131 - Twisted Project
# Server Implementation

import conf, utils
from client import ProxyClientFactory

import sys, re, os, time, json, logging

from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from twisted.web.client import getPage


class ProxyServerProtocol(LineReceiver):

  def __init__(self, factory):
    self.factory = factory
    self.at_response = "AT {}".format(factory.server_name) + " {:+f} {} {} {}"

  def connectionMade(self):
    self.factory.connections += 1
    self.infoHandler("CONNECTION ESTABLISHED; Total: {}".format(
        self.factory.connections))

  def connectionLost(self, reason):
    self.factory.connections -= 1
    self.infoHandler("CONNECTION LOST; Total: {}".format(
        self.factory.connections))

  def commandFailed(self, line):
    logging.error("INVALID COMMAND: {}".format(line))
    self.transport.write("? {}\n\n".format(line))

  def help(self, quit=False):
    help_message = "\n".join((
        "Available commands:",
        "> IAMAT [client_id] [client_position] [client_time]",
        "> WHATSAT [client_id] [radius] [bound]",
        "> AT [server_id] [time_diff] [client_id] [client_position] [client_time]",
        "> help", "> quit\n\n"))
    quit_message = "\n".join(
        ("To disconnect from the current session, use the Telnet escape",
         "character '^]' (Control-]), and then type 'quit' into the Telnet",
         "interpreter to safely close the connection.\n\n"))
    self.transport.write(help_message if not quit else quit_message)

  def errorHandler(self, error, validate=False, diff=None):
    logging.error(error)
    self.transport.write("> {}{}\n".format(diff if diff else error,
                                           "" if validate else "\n"))

  def infoHandler(self, info):
    logging.info(info)

  def lineReceived(self, line):
    self.infoHandler("LINE RECEIVED: {}".format(line))
    try:
      items = line.split()
      return {
          "IAMAT": self.processIAMAT,
          "WHATSAT": self.processWHATSAT,
          "AT": self.processAT,
          "help": lambda : self.help(),
          "quit": lambda : self.help(quit=True)
      }[items[0]](*items[1:])
    except Exception as e:
      if isinstance(e, utils.ValidationError):
        self.errorHandler(e, validate=True)
      self.commandFailed(" ".join(items))

  def stopPropagation(self, client_id, client_time):
    return client_id in self.factory.clients and self.factory.clients[
        client_id] and float(
            client_time) <= self.factory.clients[client_id]["time"]

  def propagate(self, data, exclude=""):
    data["response"] += " {}".format(self.factory.server_name)
    valid_neighbors = set(
        conf.SERVER_NEIGHBORS[self.factory.server_name]) - set(exclude)
    for neighbor in valid_neighbors:
      if neighbor in self.factory.connected_servers:
        # Queue messages that failed to send
        self.factory.connected_servers[neighbor].sendAT(data["response"])
      else:
        reactor.connectTCP(conf.SERVER_CONFIG[neighbor]["ip"],
                           conf.SERVER_CONFIG[neighbor]["port"],
                           ProxyClientFactory(self.factory, neighbor, data))
      self.infoHandler("Location update attempted from {} to {}".format(
          self.factory.server_name, neighbor))

  @utils.validate(utils.validateIAMAT)
  def processIAMAT(self, client_id, client_position, client_time):
    response = self.at_response.format(time.time() - float(client_time),
                                       client_id, client_position, client_time)
    self.transport.write("{}\n\n".format(response))
    self.infoHandler("IAMAT RESPONSE: {}".format(response))

    # Don't propagate duplicate or outdated requests
    if self.stopPropagation(client_id, client_time):
      self.infoHandler("IAMAT PROCESS: Not propagating duplicate/outdated data")
      return

    client_position = ",".join(re.findall(r"([-+]\d+\.\d+)", client_position))
    self.factory.clients[client_id] = {
        "response": response,
        "position": client_position,
        "time": float(client_time)
    }
    self.propagate(self.factory.clients[client_id])

  @utils.validate(utils.validateWHATSAT)
  def processWHATSAT(self, client_id, radius, bound):

    def processGooglePlacesQuery(response, at_message, bound):
      try:
        response_json = json.loads(response)
        response_json["results"] = response_json["results"][:bound]
      except:
        error_ = "WHATSAT PROCESS: Error processing Google Places request JSON"
        self.errorHandler("{}: {}".format(error_, response_json), diff=error_)
      else:
        client_message = "{}\n{}\n\n".format(
            at_message, json.dumps(response_json, indent=2))
        log_message = "{}\n{}".format(at_message, json.dumps(response_json))
        self.transport.write(client_message)
        self.infoHandler("WHATSAT RESPONSE: {}".format(log_message))

    def processGooglePlacesQueryError(error):
      error_ = "WHATSAT PROCESS: Error processing Google Places Request"
      self.errorHandler("{}: {}".format(error_, error.parents[0]), diff=error_)

    if client_id not in self.factory.clients or not self.factory.clients[
        client_id]:
      self.errorHandler(
          "WHATSAT REQUEST: There is no location data at server {} for client {}"
          .format(self.factory.server_name, client_id))
      return

    at_message = self.factory.clients[client_id]["response"]
    coordinates = self.factory.clients[client_id]["position"]

    query_url = conf.GOOGLE_PLACE_API_URL.format(coordinates, radius)
    self.infoHandler("Google Places query URL: {}".format(query_url))

    query_response = getPage(query_url) \
        .addCallback(processGooglePlacesQuery, at_message, int(bound)) \
        .addErrback(processGooglePlacesQueryError) \
        .addTimeout(1.0, reactor)

  @utils.validate(utils.validateAT)
  def processAT(self, server_name, time_difference, client_id, client_position,
                client_time, sender_name):
    if self.stopPropagation(client_id, client_time):
      self.infoHandler("AT PROCESS: Not propagating duplicate/outdated data")
      return

    response = self.at_response.format(time.time() - float(client_time),
                                       client_id, client_position, client_time)
    client_position = ",".join(re.findall(r"([-+]\d+\.\d+)", client_position))
    self.infoHandler("Added or updated {} at {}: {}".format(
        client_id, client_time, response))
    self.factory.clients[client_id] = {
        "response": response,
        "position": client_position,
        "time": float(client_time)
    }
    self.propagate(self.factory.clients[client_id], exclude=sender_name)


# Modeled from: https://twistedmatrix.com/documents/current/core/howto/servers.html#factories
class ProxyServerFactory(protocol.ServerFactory):

  def __init__(self, server_name, server_port):
    self.server_name = server_name
    self.server_port = server_port
    self.connections = 0
    self.clients = {}
    self.connected_servers = {}

    try:
      os.makedirs("logs")
    except OSError:
      if not os.path.isdir("logs"):
        raise

    self.log_file = "logs/server-{}.log".format(self.server_name)
    logging.basicConfig(
        filename=self.log_file,
        level=logging.DEBUG,
        filemode="a",
        format="%(asctime)s %(message)s")
    logging.info("SERVER STARTED {}:{}".format(self.server_name,
                                               self.server_port))

  def buildProtocol(self, address):
    return ProxyServerProtocol(self)

  def stopFactory(self):
    logging.info("SERVER SHUTDOWN {}:{}".format(self.server_name,
                                                self.server_port))
