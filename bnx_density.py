#! /usr/bin/env python
import sys, os
import bnx, sqlite3, datetime
import numpy

pwd=sys.path[0]
bnx_file=sys.argv[1]

density_file=bnx_file+".density"
density_plot_file=bnx_file.replace(".bnx",".density.pdf")
start_time=datetime.datetime.now()
db_file=bnx_file+".bni"

if os.path.exists(db_file)==False: bnx.createIndex(bnx_file)
start_time=datetime.datetime.now()
if os.path.exists(density_file)==False:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT Length,NumberofLabels,SNR,AvgIntensity FROM READS WHERE Length >= 150000")
    results=c.fetchall()
    out = open(density_file, "w")
    out.write("Length\tnlabels\tdensity\tSNR\tAvgIntensity")
    for i in results:
        out.write("\n"+"\t".join([str(i[0]),str(i[1]),str(100000*i[1]/i[0]),str(i[2]),str(i[3])]))
    out.write
    c.close()

os.system("Rscript "+pwd+"/density_plot.R "+density_file+" labels."+density_plot_file+" Length nlabels")
os.system("Rscript "+pwd+"/density_plot.R "+density_file+" labels2."+density_plot_file+" Length density")
os.system("Rscript "+pwd+"/density_plot.R "+density_file+" SNR."+density_plot_file+" Length SNR")
os.system("Rscript "+pwd+"/density_plot.R "+density_file+" intensity."+density_plot_file+" Length AvgIntensity")
print(bnx.runtime(start_time))