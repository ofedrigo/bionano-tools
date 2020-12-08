from subprocess import PIPE, run
import math,os
import sqlite3
import datetime, numpy

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
	
def get_headers(bnx_file):
    header_index={"run_headers":{},"data_headers":{}}
    run_headers={}
    lines = run('grep -m 1 "#rh" '+bnx_file, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    headers=(lines.stdout).replace("\n","").split("\t")
    for i in range(1,len(headers)):
        header_index["run_headers"][headers[i]]=i+1
    
    lines = run('grep -m 1 "#0h" '+bnx_file, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    headers=(lines.stdout).replace("\n","").split("\t")
    for i in range(1,len(headers)):
        header_index["data_headers"][headers[i]]=i
    return header_index

def runtime(start_time):
    time_diff=(datetime.datetime.now()-start_time)
    minutes = divmod(time_diff.total_seconds(), 60)  
    return str(round(minutes[0]))+":"+str(round(minutes[1]))

def createIndex(bnx_file):
    start_time=time.time()
    print("Indexing "+bnx_file+"...")
    db_file=bnx_file+".bni"
    sqlite3.connect(db_file)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE SCANS ([scan_id] INTEGER PRIMARY KEY)''')
    c.execute('''CREATE TABLE COHORTS ([cohort_id] INTEGER PRIMARY KEY, [Scan_ID] INTEGER)''')
    c.execute('''CREATE TABLE READS ([molecule_id] INTEGER PRIMARY KEY, [Length] REAL, [AvgIntensity] REAL,[SNR] REAL,[NumberofLabels] INTEGER,[Cohort_ID] INTEGER)''')
    print("Collecting headers...")
    header_index=get_headers(bnx_file)
    print(runtime(start_time))
    start_time=time.time()
    print("Collectiong data info...")
    lines = run('LC_ALL=C grep -n "# Run Data" '+bnx_file+" | cut -d$'\t' -f"+str(header_index["run_headers"]["RunId"]), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    scans_dict={}
    for cohortId in lines.stdout.splitlines():
        scanId=str(math.ceil(float(cohortId)/8.0))
        scans_dict.setdefault(scanId,[]).append(str(cohortId))
    for scanId in scans_dict.keys():
        c.execute ("INSERT INTO SCANS(scan_id) values (?)", (scanId,))
        for cohort_id in scans_dict[scanId]:
            c.execute ("INSERT INTO COHORTS(cohort_id,Scan_ID) values (?,?)", (cohort_id,scanId))
    print(runtime(start_time))
    start_time=time.time()
    print("Collecting reads...")
    cols=["MoleculeId","Length","AvgIntensity","SNR","NumberofLabels","RunId"]
    data_indexes=",".join([str(header_index["data_headers"][x]) for x in cols])
    lines = run('LC_ALL=C grep -n ^0 '+bnx_file+" | cut -d$'\t' -f"+data_indexes, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    for line in lines.stdout.splitlines():
        MoleculeId,Length,AvgIntensity,SNR,NumberofLabels,RunId=line.split("\t")
        c.execute ("INSERT INTO READS (molecule_Id,Length,AvgIntensity,SNR,NumberofLabels,Cohort_ID) values (?,?,?,?,?,?)", (MoleculeId,Length,AvgIntensity,SNR,NumberofLabels,RunId))
    conn.commit()
    print(bnx_file+" created.")
    print(runtime(start_time))
"""

def get_data_info(bnx_file,linetype,cohort_index):
    lines = run('LC_ALL=C grep -n '+linetype+' '+bnx_file+" | cut -d$'\t' -f"+str(cohort_index), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    data_info={}
    for cohortId in lines.stdout.splitlines():
        scanId=str(math.ceil(float(cohortId)/8.0))
        data_info.setdefault(scanId,[]).append(str(cohortId))
    return data_info

def get_reads(bnx_file,linetype,columns):
    lines = run('LC_ALL=C grep -n '+linetype+' '+bnx_file+" | cut -d$'\t' -f"+str(cohort_index), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    data_info={}
    for cohortId in lines.stdout.splitlines():
        scanId=str(math.ceil(float(cohortId)/8.0))
        data_info.setdefault(scanId,[]).append(str(cohortId))
    return data_info
    
def get_block(bnx_file,linetype):
    #get scan/cohort info
    data_info={}
    lines = run('LC_ALL=C grep -n '+linetype+' '+bnx_file, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    block=lines.stdout.splitlines()
    return block

def get_data_cols(bnx_file,indexList,block):
    data_content=get_cols(bnx_file,indexList,block)
    return data_content

def get_cols(bnx_file,indexList,block):
    data_info={}
    starts=str(block[0])
    ends=str(block[1])
    cols=",".join([str(i) for i in indexList])
    print("awk 'NR>="+starts+" &&NR<="+ends+"{print}NR>"+ends+"{exit}' "+bnx_file+" | cut -d$'\t' -f"+cols)
    lines = run("awk 'NR>="+starts+" &&NR<="+ends+"{print}NR>"+ends+"{exit}' "+bnx_file+" | cut -d$'\t' -f"+cols, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return [x.split("\t") for x in lines.stdout.splitlines()]
"""