# Introduction

This subfolder contains a Python script to process batches of files in a given folder and save a record of what files have been processed with the current timestamp.
Next time we run the same Python script, it will look for the old record and only process the updated/new files in the folder.

User needs to specified:
(1) folder path (with pattern of the files you want to process, e.g., '*.txt') -- second last line of the script
(2) batch size in which you want to process the files (e.g., maybe you want to list 10 files at a time instead of listing them one by one) -- last line of the script
(2) given a list of files, how you want to process them (example here is to simply list them, i.e., ls file1 file2 ... fileN -la) -- modify the processFun function

# Background

Icreated this script because I have a local folder of large number of data files that may be updated from time to time. 
Sometimes Id like to copy the updated new files to a gcloud VM.
This script will help me keep a record and copy only those updated since last my copy. 
For gcloud copy, if I do it file by file, it is painfully slow. Therefore I made a generator to enable me to copy a batch of files.

T Su
April 2020
