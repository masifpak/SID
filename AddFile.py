import KeyGen
import pickle
import base64


import hashlib
import sys
import json
import csv
import os
import string
import glob
# Open the file in read mode
# Open the file in read mode

import glob
import errno

client = KeyGen.SIDClient()

KG = open("secret.key", "rb").read()
print "KG: " , KG
KSE = open ("KSE.key", "rb").read()
print "KSE: ", KSE
# Create an empty dictionary
dcount = dict()
dfiles = dict()
SearchInd = dict()
fileid_dict = dict()
Map = dict()
f = open('allwords-counts.csv', 'w')
f.truncate(0)
f = open('file_count_index.csv', 'w')
f.truncate(0)
f = open('search_word_index.csv', 'w')
f.truncate(0)
f = open('add-val-map.csv', 'w')
f.truncate(0)
count = 0


def hash_word(w):
    #hash_w = hashlib.sha512(w)
    hash_w = (hashlib.sha512(w)).digest()
    return hash_w
def hash_conn_search(h_wd,search_wd):
    #h_wd = str1
    #search_wd = str2
    #return '|'.join(list(h_wd,search_wd))
    return h_wd + search_wd
def file_id (filename):
    f_id = id(filename)
    return f_id

#file_id('asiff.txt')

path = 'data/*.txt'
files = glob.glob(path)
for fpath in files:
  #print fpath



  text = open(fpath, "r")

  # Loop through each line of the file
  for line in text:
    # Remove the leading spaces and newline character
    line = line.strip()

    # Convert the characters in line to
    # lowercase to avoid case mismatch
    line = line.lower()
    ln = line.translate(None, string.punctuation)
    # Split the line into words
    words = ln.split(" ")
    #print words

    # Iterate over each word in line
    for word in words:
        #dfiles[word]=fname

        # Check if the word is already in dictionary
        if word in dcount:
            # Increment count of word by 1
            dcount[word] = dcount[word] + 1
        else:
            # Add the word to dictionary with count 1
            dcount[word] = 1
for key in list(dcount.keys()):
#    print(key, ":", dcount[key])
#print list(dcount.keys())
#wc = csv.writer(open("allkeys.csv", "aw"))
#wc.writerow([dcount])
    wc = csv.writer(open("allwords-counts.csv", "aw"))
    wc.writerow([key, dcount[key]])
#print fileid

# Print the contents of dictionary
#for key in (dcount.keys()):
#    print key


#print "First Loop End"

#for key in list(dcount.keys()):
for wd in dcount.keys():
    print "**********************************************************************************************************"
    count +=1
    print wd
    dfiles[wd] = 0
 #  print(key, ":", dcount[key])
    #wf = csv.writer(open(fname + '.csv', "w"))
#    wc = csv.writer(open("allkeys.csv", "aw"))
#    wc.writerow([key,dcount[key]])
# Print the contents of dictionary
    #for key in list(dcount.keys()):
     #   print key
        #wc.writerow([key,dcount[key]])
      #  wc.writerow([key])
   # print "Hi HIIIIIIIIIIIIIII"

    path2 = 'data/*.txt'
    files2 = glob.glob(path)
    for fpath2 in files2:
        file_name = os.path.basename(fpath2)
        fid = file_id(file_name)
        ### Creating Array of File IDs and File Names
        fileid_dict[fid] = file_name

        print fpath2
        datafiles = file(fpath2)
        for line2 in datafiles:
            #print line2
            if wd in line2:
                print wd
                dfiles[wd] += 1
                print   dfiles[wd]
                SearchInd[wd] = 0
                h_wd = hash_word(wd)
                hash_conn_search1 = hash_conn_search(h_wd,str(SearchInd[wd]))
                K_wd = base64.b64encode(client.G(KG,hash_conn_search1))
                print "Key of Wij" , K_wd
                nfiles_conn_zero = str (dfiles[wd] + 0)
                #print h_wd
                Addr_wd = base64.b64encode(client.H(K_wd,nfiles_conn_zero))
                print "Address of Wij:" , Addr_wd
                nfiles_conn_fileid = str(fid) + str(dfiles[wd])
                print 'No. of files Concatenation with File ID : ', nfiles_conn_fileid
                Val_Wij =  client.ENC(KSE, nfiles_conn_fileid)
                print "Value of Wij:" , Val_Wij
                Map [Addr_wd] = Val_Wij
                print "Map:" , count, Map
                #print "Cout: ", count
                break
                #print "key"
            else:
                print "Word is not found"
                dfiles[wd] = dfiles[wd]
                print dfiles[wd]
#for wd in list(dfiles.keys()):
#    print wd
        #print (wd, ":", dfiles[wd])
    wf = csv.writer(open('file_count_index.csv', "aw"))
    wf.writerow([wd, dfiles[wd]])

for wd in list(SearchInd.keys()):
    ws = csv.writer(open('search_word_index.csv', "aw"))
    ws.writerow([wd, SearchInd[wd]])

for wmap in Map.keys():
    #print wmap
    wmapf  = csv.writer(open('add-val-map.csv', "aw"))
    wmapf.writerow([wmap,Map[wmap]])
#print Map