            """
            if p.fetchMethod == "fetch_single_rrd":
                try:
                    for metricName in p.metricList:
                        #print ("try to collect rrd: %s, %s, %s, %s" % (queryDate, serverName, nodeName, metricName))
                        p.extractRrdData(serverName,nodeName,metricName)
                except:
                    print ("Cannot collect single rrd: %s, %s, %s, %s" % (queryDate, serverName, nodeName))
            if p.fetchMethod == "fetch_all_rrd":
                try:
                    #print "fetchMethod=",p.fetchMethod
                    #p.extractAllRrd(serverName,nodeName)
                    p.extractAllRrdToPcp(serverName,nodeName)
                except:
                    print ("Cannot collect all rrd: %s, %s, %s" % (p.queryDate, serverName, nodeName))
            if p.fetchMethod == "xport_multi_rrd":
                try:
                    #print "fetchMethod=",p.fetchMethod
                    #p.extractAllRrd(serverName,nodeName)
                    p.xportMultiRrdToPcp(serverName,nodeName)
                except:
                    print ("Cannot collect all rrd: %s, %s, %s" % (p.queryDate, serverName, nodeName))
            """
