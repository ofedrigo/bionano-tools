from subprocess import PIPE, run
import math

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

def get_cols(bnx_file,indexList,block):
    data_info={}
    starts=str(block[0])
    ends=str(block[1])
    cols=",".join([str(i) for i in indexList])
    print("awk 'NR>="+starts+" &&NR<="+ends+"{print}NR>"+ends+"{exit}' "+bnx_file+" | cut -d$'\t' -f"+cols)
    lines = run("awk 'NR>="+starts+" &&NR<="+ends+"{print}NR>"+ends+"{exit}' "+bnx_file+" | cut -d$'\t' -f"+cols, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return [x.split("\t") for x in lines.stdout.splitlines()]

def get_block(bnx_file,linetype):
    #get scan/cohort info
    data_info={}
    lines = run('grep -n '+linetype+' '+bnx_file+" | cut -f1 -d: | sort -n", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    mylist=lines.stdout.splitlines()
    return [int(mylist[0]),int(mylist[-1])]

def get_data_info(bnx_file,indexList,block):
    data_info={}
    lines=get_cols(bnx_file,indexList,block)
    for line in lines:
        cohort=line[0]
        data_info[cohort]=math.ceil(float(cohort)/8.0)
    return data_info

def get_data_cols(bnx_file,indexList,block):
    data_content=get_cols(bnx_file,indexList,block)
    return data_content