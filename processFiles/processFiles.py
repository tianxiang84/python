#!/usr/bin/env python
'''
This is a Python script to process batches of files in a given folder and save a record of what files have been processed.
Next time we run the same (this) script, it will look for the old record and only process the updated/new files.

User needs to specified:
(1) folder path (with pattern of the files you want to process, e.g., '*.txt') -- second last line of the script
(2) batch size in which you want to process the files -- last line of the script
(2) given a list of files, how you want to process them (example here is to simply list them in terminal) -- modify the processFun function

T Su
April 2020
'''

import sys
print('\nPython Version:\n{}\n'.format(sys.version))
import os
import subprocess
import json
import time
import datetime
import glob
from pytz import timezone
import pytz



#------------------#
class fileProcessor:
    '''
    A class to process the files in a given folder (self.dirPath)
    '''
    #----------------------------------#
    def __init__(self, dirPath, pattern):
        self.est = timezone('US/Eastern')

        # Assign self.dirPath
        self.dirPath=dirPath # path of the folder in which the files you want to process
        if not os.path.isdir(self.dirPath):
            print('[ERROR] Requested folder does not exists.\n')
            sys.exit()
        else:
            print('[INFO] Request received to process files in:\n{}\n'.format(os.path.join(self.dirPath,pattern)))

        # Create a list of files in current folder and their creation time
        self.currFileList=glob.glob(os.path.join(self.dirPath,pattern))
        self.currFileList.sort()
        self.genAtEnd=False

        # Check if record file exists in current folder
        currPath=os.path.abspath(__file__)
        currDir=os.path.split(currPath)[0]
        if self.dirPath[-1]=='/':
            self.recordFile=os.path.join(currDir,os.path.basename(self.dirPath[0:-1])+'.json')
        else:
            self.recordFile=os.path.join(os.path.basename(self.dirPath[0:])+'.json')

        if os.path.isfile(self.recordFile):
            # read record file
            print('[INFO] Found record file. Loading it ...\n')
            with open(self.recordFile) as f:
                self.record = json.load(f)
        else:
            # create record file
            print('[INFO] No previous record file found in current folder. Creating an empty record.\n')
            self.record=dict() # empty record



    #---------------------------------#
    def filesGenerator(self,batchSize):
        '''
        File generator to get the next batchSize of unprocessed files until all files are returned, also get the skip files in the middel
        '''
        currentID=-1
        self.genAtEnd=False

        while True:
            # Prepare yield lists
            # yieldList is the next batchSize of files to be processed (until all files returned), skipList is when including the yieldList the files we determined to skip
            yieldList=[] # files not processed to be yield
            skipList=[]  # files processed to be yield

            while True: # until we get batachSize of yieldList or reach the end
                currentID+=1

                if currentID>len(self.currFileList)-1:
                    self.genAtEnd=True
                    break

                filePath=self.currFileList[currentID]
                createTime= datetime.datetime.strptime(time.ctime(os.path.getctime(filePath)), "%a %b %d %H:%M:%S %Y")
                createTime = self.est.localize(createTime)
                createTime = createTime.astimezone(pytz.utc)
                createTime = (createTime - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

                if (os.path.split(filePath)[1] in self.record):
                    #print('In record: c-{}, p-{}'.format(createTime, record[fileBasename]['processedTime']))
                    if createTime < self.record[os.path.split(filePath)[1]]['processedTime']:
                        #print('No need to update.\n')
                        skipList.append(filePath)
                        #newRecord[fileBasename]=record[fileBasename]
                        continue

                yieldList.append(filePath)
                if len(yieldList)==batchSize:
                    if currentID==len(self.currFileList)-1:
                        self.genAtEnd=True
                    else:
                        self.genAtEnd=False
                    break

            # The 2nd while loop is jumped out here (so we've get the yielList)
            if self.genAtEnd:
                break # so we yield (2 lines down and stop)
            yield(yieldList,skipList) # not reaching the end, we yield and continue the first while loop
        yield(yieldList,skipList)



    #--------------------------------#
    def processFiles(self, batchSize):
        '''
        Process the files in batchedSize (or smaller size if we've reached the end of the file list)
        Update record
        '''
        newRecord=dict() # new record

        print('[INFO] Processing the updated or new files ...')
        gen=self.filesGenerator(batchSize)
        while not fp.genAtEnd:
            filesToProcessed, filesSkipped = next(gen)

            ## Process the files (example here is to list them)
            return_code = self.processFunc(filesToProcessed)

            # the filesToProcessed is processed succesfully, update record
            if return_code==0:
                currentTime = self.est.localize(datetime.datetime.now())
                currentTime = currentTime.astimezone(pytz.utc)
                currentTime = (currentTime - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
                for filePath in filesToProcessed:
                    newRecord[os.path.split(filePath)[1]]={'processedTime':currentTime}

            # copy old record for the skipped files
            for filePath in filesSkipped:
                newRecord[os.path.split(filePath)[1]]=self.record[os.path.split(filePath)[1]]

        print('\n[INFO] Saving new record at {} ...'.format(self.recordFile))
        with open(self.recordFile, 'w') as outfile:
            json.dump(newRecord, outfile)
        print('\n[INFO] Files processed and new record saved.')



    #--------------------------------#
    def executeBash(self,commandList):
        '''
        Given a single bash command line as a list, execute it
        '''
        process = subprocess.Popen(commandList,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            output = process.stdout.readline()
            print(output.strip())

            # Do something else
            return_code = process.poll()
            if return_code is not None:
                #print('RETURN CODE', return_code)
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    print(output.strip())
                break

        return return_code



    #-----------------------------#
    def processFunc(self,fileList):
        ## Process the files (example here is to list them)
        if len(fileList)==0:
            return 0

        ## Here as an example, we simply list the files: ls file1 file2 file3
        cm=['ls']
        for filePath in fileList:
            cm.append(filePath)
        #cm.append('-la')

        return_code=self.executeBash(cm)
        return return_code



fp = fileProcessor('/home/TSu/Projects/programmingLanguage/python/processFiles','*.txt')
fp.processFiles(10)
