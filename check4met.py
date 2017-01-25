#!/usr/bin/env python

"""check4met.py - checks is necessary met files exist for GEOS-Chem execution"""

import os
from datetime import date as date
from datetime import timedelta as td

#top level directory
metdir = '/group_workspaces/jasmin/geoschem/local_users/lsurl/GEOSdata/'
#date range of interest
first_date = date(2014, 1, 1)
last_date  = date(2014,12,31)

print "Considering subdirectories of %s" %metdir

print "Looking for files spanning dates %s to %s" %(first_date.strftime("%Y-%m-%d"),last_date.strftime("%Y-%m-%d"))

res_and_nests = ['0.25x0.3125_CH','0.25x0.3125_NA','0.25x0.3125_EU','0.25x0.3125_SE',
                 '0.5x0.666_CH','0.5x0.666_NA','0.5x0.666_EU','0.5x0.666_SE',
                 '2x25','4x5']

ftypes = ["A1","A3cld","A3dyn","A3mstC","A3mstE","I3"]

have_dict = {}




for rn in res_and_nests:
    print "========"
    print "Considering: %s" %rn
    
    rn_nodots = rn.replace("2.5","25").\
            replace("0.25","025").replace("0.3125","03125").\
            replace("0.5","05").replace("0.666","0666").\
            replace("_",".")
    
    #1. Does subdirectory exist?
    rn_path = os.path.join(metdir,"GEOS_"+rn,"GEOS_FP")
    have_dict[rn]=os.path.exists(rn_path)
    if not have_dict[rn]:
        print "No subdirectory directory exists for %s" %rn
        continue
    
    print "Subdirectory exists at: %s" %rn_path
    
    #2. Check for constant 2011-01-01 file
    
    cn_filename = "GEOSFP.20110101.CN."+rn_nodots+".nc"
    cn_path = os.path.join(rn_path,"2011","01",cn_filename)
    if os.path.isfile(cn_path):
        pass
        #print "Constant file exists: %s" %cn_path
    else:
        print "MISSING expected constant file: %s" %cn_path 
    
    #2. Main checking
    
    d = first_date
    checked_year = False
    checked_month = False
    
    while d <= last_date:
        if d.day == 1: #first day of month
            if d.month == 1: #1st January
                #check year subdirectory exists
                if not os.path.exists(os.path.join(rn_path,str(d.year))):
                    print "NO YEAR SUBDIRECTORY EXISTS for year=%i" %d.year
                    d = date(d.year+1,1,1) #jump to next 1st January
            #check month subdirectory exists
            month_subdir = os.path.join(rn_path,str(d.year),str(d.month).zfill(2))
            if not os.path.exists(month_subdir):
                print "NO MONTH SUBDIRECTORY EXISTS for month%i-%i" %(d.year,d.month)
                if d.month==12: #if December
                    d = date(d.year+1,1,1) #jump to next 1st January
                else:
                    d = date(d.year,d.month+1,1) #jump to next 1st of month
        #if we get here, there's a year and month subdirectory. Let's see if it has files for this day.
        for ftype in ftypes:
            if os.path.isfile(os.path.join(month_subdir,"GEOSFP."+str(d.year)+str(d.month).zfill(2)+str(d.day).zfill(2)+"."+ftype+"."+rn_nodots+".nc")):
                pass
                #print "%s file exists for %s" %(ftype,d.strftime("%Y-%m-%d"))
            else:
                print "%s file MISSING for %s" %(ftype,d.strftime("%Y-%m-%d"))
        d = d+td(days=1)
        
        
            

        

            
    
    


