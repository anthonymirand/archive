#!/usr/bin/env python

# Configuration file for the Twisted Places proxy herd

GOOGLE_API_KEY = "SECRET_KEY"

GOOGLE_PLACE_API_URL = "https://maps.googleapis.com/maps/api/place/" \
    "nearbysearch/json?location={}&radius={}&sensor=false&key=" + GOOGLE_API_KEY

SERVER_CONFIG = {
  "Alford"   : { "ip" : "localhost", "port" : 11500 },
  "Ball"     : { "ip" : "localhost", "port" : 11501 },
  "Hamilton" : { "ip" : "localhost", "port" : 11502 },
  "Holiday"  : { "ip" : "localhost", "port" : 11503 },
  "Welsh"    : { "ip" : "localhost", "port" : 11504 }
}

SERVER_NEIGHBORS = {
  "Alford"   : [ "Hamilton", "Welsh" ],
  "Ball"     : [ "Holiday", "Welsh" ],
  "Hamilton" : [ "Holiday", "Alford" ],
  "Holiday"  : [ "Ball", "Hamilton" ],
  "Welsh"    : [ "Alford", "Ball" ]
}
