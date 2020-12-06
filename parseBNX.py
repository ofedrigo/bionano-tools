#! /usr/bin/env python
import sys, glob,os,math
from subprocess import PIPE, run
import numpy

#!/usr/bin/python
import sys
	
def average(numlist):
	if len(numlist)>0:
		return sum(numlist)/len(numlist)
	return 0

def N50(lengths):
	all_len=sorted(lengths, reverse=True)
	csum=numpy.cumsum(all_len)
	n2=int(sum(lengths)/2)
	csumn2=min(csum[csum >= n2])
	ind=numpy.where(csum == csumn2)
	return all_len[int(ind[0])]

#bnx="RawMolecules.bnx"
bnx=sys.argv[1]
molid,runid,lentgh="","",""
results={}
rundata={}
legend_0=[]
legend_1=[]
allReads=[]
with open(bnx) as infile:
	#get first legend
	line = run('grep -m 1 "#rh" '+bnx, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	legend_0=(line.stdout).replace("\n","").split("\t")
	runid_0=legend_0.index("RunId")
	
	#get second legend
	line = run('grep -m 1 "#0h" '+bnx, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	legend_1=(line.stdout).replace("\n","").split("\t")
	length_1=legend_1.index("Length")-1
	runid_1=legend_1.index("RunId")-1
	labels=legend_1.index("NumberofLabels")-1
	
	#get scan/cohort info
	lines = run('grep "# Run Data" '+bnx, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	data=[x.split("\t") for x in lines.stdout.splitlines()]
	for items in data:
		cohort=items[runid_0]
		scan=math.ceil(float(cohort)/8.0)
		rundata[cohort]=scan
	
	#get data
	lines=run("grep ^0 "+bnx,stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	output=lines.stdout.splitlines()
	
	#parse data and grab length per scan
	for line in output:
		data=line.split("\t")
		cohort=data[runid_1]
		thislength=data[length_1]
		scan=rundata[cohort]
		thislabel=data[labels]
		allReads.append([thislength,thislabel])
		if int(float(thislength))>=150000:
			results.setdefault(scan,[]).append(int(float(thislength)))

allscans=list(results.keys())
s=0
t=[]
for scan in sorted(allscans):
	print(str(scan)+"\t"+str(average(results[scan]))+"\t"+str(N50(results[scan]))+"\t"+str(min(results[scan]))+"\t"+str(max(results[scan])))
	s=s+sum(results[scan])
	t=t+results[scan]
print(s)
print(N50(t))

out = open("RL-label.txt", "w")
out.write("RL\tLabels")
for line in allReads:
    out.write("\n"+line[0]+"\t"+line[1])
out.close()