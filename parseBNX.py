#! /usr/bin/env python
import sys, numpy
import bnx

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

#Main
bnx_file=sys.argv[1]
allReads=[]

r=bnx.get_headers(bnx_file)


#cohort_block=bnx.get_block(bnx_file,'"# Run Data"')


cohort_block=[7,174]
cohort_index=r["run_headers"]["RunId"]
rundata=bnx.get_data_info(bnx_file,[cohort_index],cohort_block)
print(rundata)


#data_block=bnx.get_block(bnx_file,"^0")

#data_block=[184, 95887860]
data_block=[184,200]

t=bnx.get_data_cols(bnx_file,[r["data_headers"]["Length"],r["data_headers"]["RunId"],r["data_headers"]["NumberofLabels"]],data_block)
print(t)


"""
molid,runid,lentgh="","",""
results={}


#get data
lines=run("grep ^0 "+bnx,stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
#parse data and grab length per scan
for line in lines.stdout.splitlines():
    items=line.split("\t")
    cohort=items[runid_index]
    scan=rundata[cohort]
    thislength=items[length_1]
    thislabel=items[labels]
    allReads.append([thislength,thislabel])
    if int(float(thislength))>=150000:
        results.setdefault(scan,[]).append(int(float(thislength)))
"""
"""
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
"""