#! /usr/bin/env python
import sys, os
import bnx, sqlite3, datetime
import numpy

pwd=sys.path[0]
#Main
bnx_file=sys.argv[1]
SNR_dist_file=bnx_file+".SNR.dist"
SNR_scan_file=bnx_file+".SNR"
db_file=bnx_file+".bni"
SNR_plot_file=bnx_file.replace(".bnx",".SNR.scan.pdf")
SNR_histo_file=bnx_file.replace(".bnx",".SNR.dist.pdf")
if os.path.exists(db_file)==False: bnx.createIndex(bnx_file)

start_time=datetime.datetime.now()
if os.path.exists(SNR_scan_file)==False:
    #get read lengths per scan
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT scan_id FROM SCANS")
    scans=[str(x[0]) for x in c.fetchall()]

    out = open(SNR_scan_file, "w")
    out.write("scanId\tnreads\tmean\tN50")
    all_SNR=[]
    for thisscan in scans:
        c.execute("SELECT cohort_id FROM COHORTS WHERE Scan_ID=?",(thisscan,))
        cohorts=",".join([str(x[0]) for x in c.fetchall()])
        c.execute("SELECT molecule_id,Length,SNR FROM READS WHERE Cohort_ID IN ("+cohorts+")")
        results=c.fetchall()
        signal_list=[]
        for x in results:
            length=float(x[1])
            SNR=float(x[2])
            if length>150000:
                signal_list.append(SNR)
                all_SNR.append(SNR)
        out.write("\n"+"\t".join([str(thisscan),str(len(results)),str(bnx.average(signal_list)),str(bnx.N50(signal_list))]))
        print("scan #"+str(thisscan)+" processed.")
    out.close()
    c.close()
    out = open(SNR_dist_file, "w")
    hist,bins=numpy.histogram(all_SNR, bins = 100)
    out.write("val\tbin")
    for i in range(len(hist)):
        out.write("\n"+str(hist[i])+"\t"+str(round(bins[i])))
    out.close()
os.system("Rscript "+pwd+"/scans_plot.R "+SNR_scan_file+" "+SNR_plot_file)
os.system("Rscript "+pwd+"/histo_plot.R "+SNR_dist_file+" "+SNR_histo_file)
print(bnx.runtime(start_time))