#!/usr/bin/env python3

import math
import rmlines
from xml.dom import minidom

f='af58f4d2-31f6-40d5-a1b5-a7bb9edff2c6.rm'
rm=rmlines.RMLines.from_bytes(open(f, 'rb'))

doc=minidom.Document()

style='fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1'

nextIds={}
def getId(tag):
    id=nextIds.get(tag, 1)
    nextIds[tag]=(id+1)
    return f"{tag}{id}"

def points(stroke):
    for segment in stroke.objects:
        yield (segment.x, segment.y)

def paths(layer):
    for stroke in layer.objects:
        p=doc.createElement('path')
        p.setAttribute('id', getId('path'))
        d='M ' + ' '.join(points(stroke))
        p.setAttribute('d', d)
        p.setAttribute('style', style)
        yield p

def groups(rm):
    for layer in rm.objects:
        g=doc.createElement('g')
        g.setAttribute('id', getId('layer'))
        for p in paths(layer):
            g.appendChild(p)
        yield g

def svg(rm):
    svg=doc.createElement('svg')
    svg.setAttribute('viewBox', '0 0 1404 1872')
    doc.appendChild(svg)

    for g in groups(rm):
        svg.appendChild(g)
    return svg

svg(rm)

print(doc.toprettyxml(indent="  "))
