#! /usr/bin/env python
import sys, os
import bnx, sqlite3, datetime
import numpy

pwd=sys.path[0]
#Main
bnx_file=sys.argv[1]
labels_scan_file=bnx_file+".labels"
labels_dist_file=bnx_file+".labels.dist"
db_file=bnx_file+".bni"
labels_plot_file=bnx_file.replace(".bnx",".labels.scan.pdf")
labels_histo_file=bnx_file.replace(".bnx",".labels.dist.pdf")
if os.path.exists(db_file)==False: bnx.createIndex(bnx_file)

start_time=datetime.datetime.now()
if os.path.exists(labels_scan_file)==False:
    #get read lengths per scan
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT scan_id FROM SCANS")
    scans=[str(x[0]) for x in c.fetchall()]

    out = open(labels_scan_file, "w")
    out.write("scanId\tnreads\tmean\tN50")
    all_labels=[]
    for thisscan in scans:
        c.execute("SELECT cohort_id FROM COHORTS WHERE Scan_ID=?",(thisscan,))
        cohorts=",".join([str(x[0]) for x in c.fetchall()])
        c.execute("SELECT molecule_id,Length,NumberofLabels FROM READS WHERE Cohort_ID IN ("+cohorts+")")
        results=c.fetchall()
        labels_list=[]
        for x in results:
            length=float(x[1])
            nlabels=float(x[2])
            if length>150000:
                labels_list.append(100000*nlabels/length)
                all_labels.append(100000*nlabels/length)
        out.write("\n"+"\t".join([str(thisscan),str(len(results)),str(bnx.average(labels_list)),str(bnx.N50(labels_list))]))
        print("scan #"+str(thisscan)+" processed.")
    out.close()
    c.close()
    out = open(labels_dist_file, "w")
    hist,bins=numpy.histogram(all_labels, bins = 100)
    out.write("val\tbin")
    for i in range(len(hist)):
        out.write("\n"+str(hist[i])+"\t"+str(round(bins[i])))
    out.close()
os.system("Rscript "+pwd+"/scans_plot.R "+labels_scan_file+" "+labels_plot_file)
os.system("Rscript "+pwd+"/histo_plot.R "+labels_dist_file+" "+labels_histo_file)
print(bnx.runtime(start_time))