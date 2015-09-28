#! /usr/bin/python
# -*- coding: utf-8 -*-

import lxml
from lxml import etree

if __name__ == "__main__":
    import sys, os

    if len(sys.argv) != 2:
        print "Usage: %s document.xml" % (sys.argv[0])
        exit(0)

    with open(sys.argv[1]) as f:
        doc = etree.parse(f)

    # rename tags
    for node in doc.findall(".//maxKbps"):
      node.tag = "maxSpeed"

    for node in doc.findall(".//feed"):
      node.tag = "feedTag"

    # rename attributes
    for node in doc.findall(".//*[@label]"):
      node.set("text", node.get("label"))
      del node.attrib["label"]

    # rename attributes
    for node in doc.findall(".//*[@marketID]"):
      node.set("marketType", node.get("marketID"))
      del node.attrib["marketID"]

    print etree.tostring(doc, pretty_print=True)