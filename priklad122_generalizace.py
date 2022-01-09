import matplotlib.pyplot as plt
import visvalingamwyatt as vw
from math import sqrt
import json
with open("input_d1.geojson", encoding="utf-8") as a:
    silnice = json.load(a)

def pythagorova_veta(x1, y1, x2, y2):
    prepona = sqrt((x1-x2)**2+(y1-y2)**2)
    return prepona
def heron (a,b,c):
    s=(a+b+c)/2
    area=sqrt(s*(s-a)*(s-b)*(s-c))
    return area


vertices=silnice['features'][0]['geometry']['coordinates']
before=zip(*vertices)


max_area=0.001
lenghts=[]
pricky=[]
areas=[]
for i in range(1, len(vertices)):
    v1 = vertices[i-1]
    v2 = vertices[i]
    d=pythagorova_veta(*v1, *v2)
    lenghts.append(d)
for i in range (2, len(vertices)):
    w1 = vertices[i-2]
    w2 = vertices[i]
    c=pythagorova_veta(*w1, *w2)
    pricky.append(c)
for i in range (1, len(lenghts)):
    a=lenghts[i-1]
    b=lenghts[i]
    c=pricky[i-1]
    area=heron (a,b,c)
    areas.append(area)

while len(areas)>=1 and min(areas)<max_area:
    rank=areas.index(min(areas))
    
    vertices.pop(rank+1)
    lenghts[rank]=pricky[rank]
    lenghts.pop(rank+1)
    if rank!=0:
        pricky[rank-1]=pythagorova_veta(*vertices[rank-1],*vertices[rank+1])
        areas[rank-1]=heron(lenghts[rank-1],lenghts[rank],pricky[rank-1])
    pricky.pop(rank)
    areas.pop(rank)
    if rank!=(len(areas)):
        pricky[rank]=pythagorova_veta(*vertices[rank],*vertices[rank+2])
        areas[rank]=heron(lenghts[rank+1],lenghts[rank],pricky[rank])

kontrola=vw.simplify(vertices,threshold=max_area)
print (kontrola)
print(vertices)

after=zip(*vertices)
plt.figure()
plt.plot(*before)
plt.plot(*after)
plt.show()
