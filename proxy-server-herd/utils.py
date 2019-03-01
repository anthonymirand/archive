#!/usr/bin/env python

# CS 131 - Twisted Project
# Utils for input validation

import re


class ValidationError(Exception):
  pass


def validate(validationHandler):
  def real_decorator(func):
    def wrapper(self, *args, **kwargs):
      try:
        validationHandler(args, **kwargs)
      except:
        raise
      else:
        func(self, *args, **kwargs)
    return wrapper
  return real_decorator


def validateIAMAT(data, check="IAMAT"):
  if len(data) != 3:
    raise ValidationError("{} LENGTH: {} does not have three fields".format(
        check, data))
  try:
    validateGPS(data[1], check=check)
  except:
    # Exception formatting done in validateGPS function
    raise
  try:
    time = float(data[2])
  except:
    raise ValidationError("{} TIME: {} is not a valid POSIX time".format(
        check, data[2]))


def validateWHATSAT(data):
  if len(data) != 3:
    raise ValidationError(
        "WHATSAT LENGTH: {} does not have three fields".format(data))
  try:
    if int(data[1]) < 0 or 50 < int(data[1]):
      raise ValidationError(
          "WHATSAT RADIUS: {} not in valid range (0, 50)".format(data[1]))
    if int(data[2]) < 0 or 20 < int(data[2]):
      raise ValidationError(
          "WHATSAT BOUND: {} not in valid range (0, 20)".format(data[2]))
  except:
    raise ValidationError(
        "WHATSAT ARGS: {} or {} are not valid integer parameter(s)".format(
            data[1], data[2]))


def validateAT(data):
  if len(data) != 6:
    raise ValidationError("AT LENGTH: {} does not have six fields".format(data))
  try:
    client_time = float(data[1])
  except:
    raise ValidationError("AT TIME: {} is not valid POSIX time".format(data[1]))
  try:
    validateIAMAT(data[2:-1], check="AT")
  except:
    # Exception formatting done in validateIAMAT function
    raise


def validateGPS(data, check):
  try:
    coords = re.findall(r"([-+]\d+\.\d+)", data)
    lat, lon = map(float, coords)
    if lat < -90 or 90 < lat or lon < -180 or 180 < lon:
      raise ValidationError(
          "{} GPS FORMAT: {} are not valid coordinates per ISO 6709".format(
              check, ",".join(coords)))
  except:
    raise ValidationError(
        "{} GPS FORMAT: {} is not a correctly formatted pair of coordinates".
        format(check, data))
