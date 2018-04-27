'''
Author: Alex Shannon, NYU CUSP, May 2018

This script takes as input a directory path ('the origin'), and moves
the last file created/added to that directory to a specified destination
whose path is saved as an environmental variable called FILEDESTINATION.
The script checks for new files continuously at 30 seconds intervals.

The script returns a message and timestamp on each successful run; the
message will inform whether a file has been moved or whether the origin
folder is empty (and thus no files were moved on that run).
'''

import datetime
import glob
import os
import sched
import shutil
import sys
import time

if 'FILEDESTINATION' not in os.environ:
    sys.exit('Environmental Variable \'FILEDESTINATION\' undefined')

ORIGIN = str(sys.argv[1])
FILEDESTINATION = os.environ['FILEDESTINATION']
SECONDS_BETWEEN_RUNS = 30

def find_latest_file(origin):
    '''
    Takes directory path of origin.
    Returns the last file created in the origin.
    '''
    list_of_files = glob.glob(origin + '/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return (latest_file)

def move_to_FILEDESTINATION(latest_file):
    '''
    Takes a string of the path of the latest file in the origin.
    Moves that file to the folder specified by the environmental
    variable FILEDESTINATION.
    '''
    latest_file_short = latest_file.split('/')[-1]
    destination = (FILEDESTINATION + '/' + latest_file_short)
    destination = destination.replace('//', '/')
    shutil.move(latest_file, FILEDESTINATION + '/' + latest_file_short)

def run_script(origin):
    '''
    Takes directory path of the origin.
    Runs the above modules, moving files from the origin directory 
    to the destination, otherwise printing that no files exist, and
    so nothing was moved on the current run-through. Repeats 
    recursively with the interval SECONDS_BETWEEN_RUNS until stopped 
    by the user in bash. 
    '''
    # possible errors if origin is empty
    empty_file_msg_1 = 'local variable \'latest_file\' referenced before \
                          assignment'
    empty_file_msg_2 = 'max() arg is an empty sequence'
    
    # assign latest file unless origin is empty
    try:
        latest_file = find_latest_file(str(origin))
    except (ValueError, UnboundLocalError) as err:
        if str(err) == empty_file_msg_1 or str(err) == empty_file_msg_2:
            print('The directory provided is empty; no files were moved.' \
                  + '\nUTC_time:' + str(datetime.datetime.utcnow()) + '\n')
            s.enter(SECONDS_BETWEEN_RUNS, 1, run_script, (origin,))  # repeats
            return  # terminates
        else:
            print ('VALUE ERROR:', err)
            return  # terminates
    
    # move file, raise errors if necessary
    try:
        move_to_FILEDESTINATION(latest_file)
    except FileNotFoundError as err:
        print ('FILE NOT FOUND ERROR:', err)
        return  # terminates
    
    # print details if successful run
    print('File ' + latest_file + ' successfully moved to ' + FILEDESTINATION \
                  + '\nUTC_time:'+ str(datetime.datetime.utcnow()) + '\n')
    s.enter(SECONDS_BETWEEN_RUNS, 1, run_script, (origin,))  # repeats

# runs the above code at selected interval, 'SECONDS_BETWEEN_RUNS'
s = sched.scheduler(time.time, time.sleep)
run_script(ORIGIN)
s.run()