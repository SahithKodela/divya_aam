import os
import csv
from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
l=[]
m=[]
n=[]
p=[]
p2=[]
p3=[]
p4=[]
p5=[]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def dash_view(request):
    global l,m,n
    l=[]
    m=[]
    n=[]
    file = os.path.join(os.path.join(BASE_DIR, "graph"),'Top_lanes.csv')
    file1 = os.path.join(os.path.join(BASE_DIR, "graph"),'FMC_data_1.csv')
    csv_file = open(file, 'r')
    csv_file1 = open(file1, 'r')
    x = csv.reader(csv_file, delimiter=',')
    x1 = csv.reader(csv_file1, delimiter=',')
    d=str(request.GET.get("d"))
    f = str(request.GET.get("start")).upper()
    t = str(request.GET.get("end")).upper()
    c = f + "->" + t
    filtered = [row for row in x if row[1] == d and row[0] == c]
    filtered1 = [row for row in x1 if row[3] == d and row[2] == c]
    for i in filtered:
        o = i[2].split(" ")
        l.append(o[0])
        m.append(float(i[3]))
        n.append(float(i[4]))
        p2.append(float(i[5]))
        p3.append(float(i[6]))
        p4.append(float(i[7]))
        p5.append(float(i[8]))
    n1=[]
    n2 = []
    row = False
    for i in filtered1:
        if i[5] != '':
            n1.append(float(i[5]))
    for i in filtered1:
        if i[5]=='':
            i[5]='Canceled'
        if i[4]==i[8] and i[9]=='AM':
            i[8]='----'
            i[9]='----'
        n2.append([i[0],i[1],i[4],i[5],i[7],i[8],i[9]])
    svl=[i for i in filtered if i[2]=='01:00 PDT']
    if n2:
        for i in n2:
            if i[1]=='FindWork':
                i[1]='Adhoc booked'
                row = True
            else:
                i[1]=''

    try:
        sv=float(svl[0][4])
    except:
        sv=0
    sum1=sum(n1)#+sum(n)
    fv = sv - sum1
    if n2:
        xuv=n2[0][2]
    else:
        xuv=0
    for i in n2:
        x = i[-2].split(':')
        if n2[-1]=='PM':
            if int(x[1]):
                x[0]=int(x[0])+1
            x1 = int(x[0])+12
            x[0]=x1
        x.pop()
        i[-2] = ':'.join(x)
        if i[-3]==d:
            p.append(i[-2])
    context={'c':c,'d':d,'cpt':n2,'sum':sum1,'fv':fv,'sv':sv,'cpt1':xuv,'row':row}
    return render(request,"dash.html",context)
# Create your views here.
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):
        usernames =(l,m,n,p,p2,p3,p4,p5)
        return Response(usernames)
