#!/usr/bin/env python3

import math
import rmlines
f='af58f4d2-31f6-40d5-a1b5-a7bb9edff2c6.rm'
rm=rmlines.RMLines.from_bytes(open(f, 'rb'))

def angle(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return math.atan2(y2-y1, x2-x1) * 180 / math.pi

def lines(rm):
    for layer in rm.objects:
        for stroke in layer.objects:
            points=[]
            line=None
            for segment in stroke.objects:
                points.append((segment.x, segment.y))
                if len(points) > 1:
                    segmentAngle=angle(points[-2], points[-1])
                    if len(points) == 2:
                        line=(points[0], points[1])
                    else:
                        lineAngle=angle(*line)
                        if abs(segmentAngle-lineAngle) < 10:
                            line=(points[0], points[-1])
                        else:
                            yield line
                            points=[]
                            line=None

for line in lines(rm):
    print(line)
