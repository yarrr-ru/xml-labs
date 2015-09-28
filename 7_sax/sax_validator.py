#! /usr/bin/python
# -*- coding: utf-8 -*-

import lxml
import re
from lxml import etree
from enum import Enum

class XmlType(Enum):
    tag = "tag"
    attr = "attr"

class Rule(object):
    def __init__(self, xmlType=None, pattern=None, minOccurs=None, maxOccurs=None):
        self._xmlType = xmlType
        self._pattern = pattern
        self._minOccurs = minOccurs
        self._maxOccurs = maxOccurs

        self._patternCompiled = None
        if not pattern is None:
            self._patternCompiled = re.compile(pattern)
        self._actualOccurs = 0

    def validate(self, actualXmlType, actualText):
        if not self._xmlType is None and self._xmlType != actualXmlType:
            raise ValueError("Expect xmlType: {}, actual: {}".format(
                self._xmlType, actualXmlType))

        if not self._patternCompiled is None and not self._patternCompiled.match(actualText):
            raise ValueError("Expect pattern: {}, actual: {}".format(
                self._pattern, actualText))

        self._actualOccurs += 1

        if not self._maxOccurs is None and self._maxOccurs < self._actualOccurs:
            raise ValueError("Expect maxOccurs: {}, actual: {}".format(
                self._maxOccurs, self._actualOccurs))

    def clear(self):
        if not self._minOccurs is None and self._minOccurs > self._actualOccurs:
            raise ValueError("Expect minOccurs: {}, actual: {}".format(
                self._minOccurs, self._actualOccurs))

        self._actualOccurs = 0

if __name__ == "__main__":
    import sys, os

    if len(sys.argv) != 2:
        print "Usage: %s document.xml" % (sys.argv[0])
        exit(0)

    rules = {
        "configuration/Description":
            Rule(xmlType=XmlType.tag),

        "configuration/ConfigTemplates" :
            Rule(xmlType=XmlType.tag),

        "configuration/MarketDataGroup" :
            Rule(xmlType=XmlType.tag),

        "configuration/type" :
            Rule(xmlType=XmlType.attr, pattern="\w+"),

        "configuration/label" :
            Rule(xmlType=XmlType.attr, pattern="\w+"),

        "configuration/ConfigTemplates/connection/maxKbps" :
            Rule(xmlType=XmlType.tag, pattern="\d+"),

        "configuration/ConfigTemplates/connections/connection" :
            Rule(xmlType=XmlType.tag),

        "configuration/ConfigTemplates/connection/type" :
            Rule(xmlType=XmlType.tag, pattern="\w+"),

        "configuration/ConfigTemplates/connection/maxKbps" :
            Rule(xmlType=XmlType.tag, pattern="\d+"),

        "configuration/MarketDataGroup/feedType" :
            Rule(xmlType=XmlType.attr, pattern="\w+"),  

        "configuration/MarketDataGroup/marketID" :
            Rule(xmlType=XmlType.attr, pattern="\w+"),  

        "configuration/MarketDataGroup/marketDepth" :
            Rule(xmlType=XmlType.attr, pattern="\d+"),   

        "configuration/MarketDataGroup/label" :
            Rule(xmlType=XmlType.attr, pattern="\w+"), 

        "configuration/MarketDataGroup/connections/connection" :
            Rule(xmlType=XmlType.tag, minOccurs=1),   

        "configuration/MarketDataGroup/connections/connection/type" :
            Rule(xmlType=XmlType.tag, pattern="\w+"),  

        "configuration/MarketDataGroup/connections/connection/protocol" :
            Rule(xmlType=XmlType.tag, pattern="\w+"),  

        "configuration/MarketDataGroup/connections/connection/src-ip" :
            Rule(xmlType=XmlType.tag, pattern="([0-9]*\.){3}[0-9]*", maxOccurs=1), 

        "configuration/MarketDataGroup/connections/connection/ip" :
            Rule(xmlType=XmlType.tag, pattern="([0-9]*\.){3}[0-9]*", maxOccurs=1), 

        "configuration/MarketDataGroup/connections/connection/port" :
            Rule(xmlType=XmlType.tag, pattern="\d+"), 

        "configuration/MarketDataGroup/connections/connection/maxKbps" :
            Rule(xmlType=XmlType.tag, pattern="\d+"), 

        "configuration/MarketDataGroup/connections/connection/feed" :
            Rule(xmlType=XmlType.tag, pattern="\w+")
    }

    stack = []

    with open(sys.argv[1]) as f:
        try:
            for event, elem in etree.iterparse(f, events=("start", "end")):
                if event == "start":
                    stack.append(elem.tag)
                    xpath = '/'.join(stack)

                    rule = rules.get(xpath, None)
                    if not rule is None:
                        rule.validate(XmlType.tag, elem.text)

                    for k, v in elem.attrib.iteritems():
                        xpath = '/'.join(stack + [k])
                        rule = rules.get(xpath, None)
                        if not rule is None:
                            rule.validate(XmlType.attr, v)
                else:
                    assert event == "end"

                    xpath = '/'.join(stack)

                    rule = rules.get(xpath, None)
                    if not rule is None:
                        rule.clear()

                    for k, v in elem.attrib.iteritems():
                        xpath = '/'.join(stack + [k])
                        rule = rules.get(xpath, None)
                        if not rule is None:
                            rule.clear()

                    stack = stack[:-1]
        except ValueError as e:
            print e
            exit(1)

        print "Document OK"
