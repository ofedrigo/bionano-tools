#! /usr/bin/env python
import sys, os
import bnx, sqlite3, datetime
import numpy

pwd=sys.path[0]
bnx_file=sys.argv[1]

RL_scan_file=bnx_file+".RL.scan"
RL_dist_file=bnx_file+".RL.dist"
yield_dist_file=bnx_file+".yield.dist"
db_file=bnx_file+".bni"
RL_plot_file=bnx_file.replace(".bnx",".RL.scan.pdf")
RL_histo_file=bnx_file.replace(".bnx",".RL.dist.pdf")
yield_plot_file=bnx_file.replace(".bnx",".yield.scan.pdf")
yield_histo_file=bnx_file.replace(".bnx",".yield.dist.pdf")

if os.path.exists(db_file)==False: bnx.createIndex(bnx_file)

start_time=datetime.datetime.now()
if os.path.exists(RL_scan_file)==False:
    #get read lengths per scan
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT scan_id FROM SCANS")
    scans=[str(x[0]) for x in c.fetchall()]
    all_reads=[]
    out = open(RL_scan_file, "w")
    out.write("scanId\tnreads\tmean\tN50\tyield")
    for thisscan in scans:
        c.execute("SELECT cohort_id FROM COHORTS WHERE Scan_ID=?",(thisscan,))
        cohorts=",".join([str(x[0]) for x in c.fetchall()])
        c.execute("SELECT molecule_id,Length FROM READS WHERE Cohort_ID IN ("+cohorts+")")
        results=c.fetchall()
        length_list=[]
        for x in results:
            length=float(x[1])
            if length>150000:
                length_list.append(length)
                all_reads.append(length)
        out.write("\n"+"\t".join([str(thisscan),str(len(results)),str(bnx.average(length_list)),str(bnx.N50(length_list)),str(sum(length_list))]))
        print("scan #"+str(thisscan)+" processed.")
    out.close()
    c.close()
    out = open(RL_dist_file, "w")
    hist,bins=numpy.histogram(all_reads, bins = 100)
    out.write("val\tbin")
    for i in range(len(hist)):
        out.write("\n"+str(hist[i])+"\t"+str(round(bins[i])))
    out.close()
os.system("Rscript "+pwd+"/scans_plot.R "+RL_scan_file+" "+RL_plot_file)
os.system("Rscript "+pwd+"/histo_plot.R "+RL_dist_file+" "+RL_histo_file)
os.system("Rscript "+pwd+"/scans_plot2.R "+RL_scan_file+" "+yield_plot_file)
print(bnx.runtime(start_time))

