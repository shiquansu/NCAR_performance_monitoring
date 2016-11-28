#!/usr/bin/env python

import os
import sys
import re
import json
import ast
import subprocess
import bisect
import time
import glob

class convertRrdToPCPArchive(object):
    """Example class that extract rrd record into local human readable files"""
    def __init__(self,fname,Date,inDir):
        print "RTfname,queryDate",fname,Date

        self.nodeListFile=fname+"-NodeList-all.txt"
        self.RRDsListFile=fname+"-RRDsList.txt"

        self.nodeDict={}
        self.metricList=[]
        self.machine=fname
        self.queryDate=Date

        self.inputDir=inDir
        self.outputDir="/home/xdmod/data/pcp-logs/yellowstone"
        self.rrdDate=Date[6:]+'.'+Date[4:6]+'.'+Date[0:4]

        self.fetchMethod="xport_multi_rrd_remote"
        self.scriptName="expectScript-"+fname+"-"+self.fetchMethod
        self.homePath="/home/xdmod/NCAR_performance_monitoring/"
        self.dataPath="/home/xdmod/data/"
        self.dailyEntryNumber=288
        self.outputDirectory=""


    def readNodeDictionary(self):
        print "fetch {ysadmin1:[node1, node2,...],ysadmin2:[node1, node2,...]}"
        f = open(self.nodeListFile, 'r')
        md={}
        md=eval(f.readline())
        for tm in md[self.machine]:
            self.nodeDict[tm]=md[self.machine][tm]

        #self.nodeDict={}
        #self.nodeDict['ysadmin4']=['ys4143']

    def buildPCPArchiveDir(self):
        #build yellowstone/ysXXXX-ib /path/to/pcp-logs/
        if os.path.exists(self.outputDir):
            sys.exit("Before continue, please backup: "+self.outputDir) 
        if os.path.exists(self.outputDir+"-empty"):
            print "copy from the empty dir\n"
        else:
            print "create the empty dir\n"
            os.system('mkdir '+self.outputDir+'-empty')
            for serverName in self.nodeDict.keys():
                for nodeName in self.nodeDict[serverName]:
                    os.system('mkdir '+self.outputDir+'-empty/'+nodeName+'-ib')
        os.system('cp -r '+self.outputDir+'-empty '+self.outputDir)
        pass

    def runConvertion(self, sName, nName):
        print "serverName, nodeName=", sName, nName
        gcommand="perl ganglia2pcp-20160906.pl -s "+self.queryDate+" -e "+self.queryDate+" -f "+self.queryDate+".00.00 -d "+self.outputDir+"/"+nName+"-ib -a "+sName+" -h "+nName+" "+self.inputDir+"/"+self.queryDate
        tmpout=os.system(gcommand)
        

def runSysCommand(scommand):
    tmpscreenout=subprocess.Popen(scommand,
                 shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT, close_fds=True)
    #tmp_array=tmpscreenout
    tmp_array=tmpscreenout.stdout.readlines()
    #print tmp_array
    return tmp_array

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("usage %s machinename (there are files in the same folder, named with machine name, containing json format resource table) queryDate(yyyymmdd) inputDir(/path/to/rrd_fetched) " % (sys.argv[0]))
        sys.exit(1)

    print "start processing resourceTable, queryDate, inputDir: "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+"\n"

    p = convertRrdToPCPArchive(sys.argv[1],sys.argv[2],sys.argv[3])
    p.readNodeDictionary()
    #p.buildPCPArchiveDir()
    for serverName in p.nodeDict.keys():
        for nodeName in p.nodeDict[serverName]:
            #pass
            p.runConvertion(serverName, nodeName)
        pass
