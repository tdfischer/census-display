#!/usr/bin/env python
import logging
import requests
from xml.etree import ElementTree
from PyQt4 import QtCore, QtGui

class Concept(object):
  def __init__(self, node):
    self._node = node

  @property
  def name(self):
    return self._node.attrib['name']
  
  def variables(self):
    for variable in self._node:
      yield Variable(variable)

class Variable(object):
  def __init__(self, node):
    self._node = node

  @property
  def name(self):
    return self._node.attrib['name']
  
  @property
  def concept(self):
    return self._node.attrib['concept']

  @property
  def description(self):
    return self._node.text

class Dataset(object):
  def __init__(self, name):
    self._url = "http://www.census.gov/developers/data/%s.xml"%(name)
    self._data = ElementTree.fromstring(requests.get(self._url).text.encode('ascii', 'ignore'))

  def concepts(self):
    root = self._data
    for concept in root:
      yield Concept(concept)

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  d = Dataset("2000_sf3")
  for c in d.concepts():
    for v in c.variables():
      print v.name, v.description
