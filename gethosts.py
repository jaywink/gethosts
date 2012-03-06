#! /usr/bin/env python

#################################################################
#                                                               #
#   Gethosts.py                                                 #
#   v0.1.1                                                      #
#                                                               #
#   Script to update /etc/hosts with newest hosts information   #
#   from the mvps.org maintained hosts list.                    #
#                                                               #
#   Author: Jason Robinson (http://www.basshero.org), 2010-2011 #
#                                                               #
#   NOTE! Before running this script, clear out any earlier     #
#   definitions from mvps.org, if any. After running this, do   #
#   not add any definitions manually after the                  #
#   SCRIPT_IDENTIFIER -line. Any content below that line will   #
#   be overwritten.                                             #
#                                                               #
#################################################################

import os, sys

# declarations
HOSTS_FILE='hosts.txt'
HOSTS_URL='http://winhelp2002.mvps.org/hosts.txt'
LOCAL_HOSTS='/etc/hosts'
TMP_PATH='/tmp'
SCRIPT_IDENTIFIER = '############# BELOW ADDED BY GETHOSTS.PY ################'

# check if we have write access to tmp
if not os.access(TMP_PATH,os.W_OK):
    sys.exit('No write access to tmp, please run as root')

# change to tmp
os.chdir(TMP_PATH)

# make sure no old hosts files exist
if os.access(HOSTS_FILE,os.F_OK):
    os.remove(HOSTS_FILE)

# get newest version of hosts list
os.system('wget -O '+HOSTS_FILE+' '+HOSTS_URL)

# make sure we received a new file
if not os.access(HOSTS_FILE,os.F_OK):
    sys.exit('Failed to receive a new hosts file, exiting')

# check that we have access to system hosts file
if not os.access(LOCAL_HOSTS,os.W_OK):
    sys.exit('No write access to '+LOCAL_HOSTS+', please run as root')
    
# copy old hosts to new file, excluding any configs copied by this script
reader = open(LOCAL_HOSTS,'r')
writer = open(LOCAL_HOSTS+'.tmp','w')
first_time = True
for row in reader:
    if row.strip('\n\r') == SCRIPT_IDENTIFIER:
        writer.write(row)
        first_time = False
        break
    else:
        writer.write(row)
reader.close()

# if this is the first time we add the content, add script identifier and also add an empty line
if first_time == True:
    writer.write('\n'+SCRIPT_IDENTIFIER+'\n\n')
else:
    writer.write('\n')
    
# write contents of new hosts file  
reader = open(HOSTS_FILE,'r')
for row in reader:
    row = row.strip('\n\r')
    writer.write(row+'\n')   
reader.close()
writer.close()

# remove new hosts file
os.remove(HOSTS_FILE)

# replace old hosts file with new version
os.system('mv -f '+LOCAL_HOSTS+'.tmp '+LOCAL_HOSTS)
