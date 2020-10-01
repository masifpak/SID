import KeyGen

import base64

import csv
import os
import string
import glob
# Open the file in read mode
# Open the file in read mode

import glob
import errno
class AddFileClass():
    def AddFile(self):
        client = KeyGen.SIDClient()
        client.clean()
        client.Client_Key_Pair()
        client.KG()
        client.Generate_KSE()
        KG = open("secret.key", "rb").read()
        print "KG: " , KG
        KSE = open ("KSE.key", "rb").read()
        print "KSE: ", KSE
        wf = csv.writer(open('file_count_index.csv', "aw"))
        ws = csv.writer(open('search_word_index.csv', "aw"))
        wmapf = csv.writer(open('add-val-map.csv', "aw"))

        '''A dictionary having words and no. of files in which that word exist'''
        dfiles = dict()
        '''A dictionary which have words and no. of files each word exist in'''
        dcount = dict()
        ### Dictionary to have no. of searches of a word
        SearchInd = dict()
        ## A dictionary to have file_id as keys and filename as values
        fileid_dict = dict()
        ## This dictionary save addresses and encrypted value of concatenation of fileids and word exist in no. of files
        Map = dict()

        ## To verify loop run as many times as no. of total words
        count = 0
        #file_id('asiff.txt')

        path = 'data/*.txt'
        files = glob.glob(path)
        stopwords = ['what', 'who', 'is', 'a', 'at', 'is', 'he', 'are', 'am', 'in', 'out', 'on', 'of', 'with', 'for', 'so', 'into', ' ']
        for fpath in files:

            text = open(fpath, "r")
            # Loop through each line of the file
            for line in text:
                # Remove the leading spaces and newline character
                strip_line = line.strip()
                # Convert the characters in line to lowercase to avoid case mismatch
                #line = line.lower()
                punch_line = strip_line.translate(None, string.punctuation)
                ''' Split the line into words'''
                words = punch_line.split(" ")
                '''Iterate over each word in line '''
                for word in words:
                    if word not in stopwords:
                    #dfiles[word]=fname
                    # Check if the word is already in dictionary
                        if word in dcount:
                            # Increment count of word by 1
                            dcount[word] = dcount[word] + 1
                        else:
                            # Add the word to dictionary with count 1
                            dcount[word] = 1
        for key in list(dcount.keys()):
            wc = csv.writer(open("allwords-counts.csv", "aw"))
            wc.writerow([key, dcount[key]])
        print "All words have listed withn their counts in all files"

        for wij in list(dcount.keys()):
            print "**********************************************************************************************************"
            count +=1
            print wij
            dfiles[wij] = 0
            SearchInd[wij] = 0
            ws.writerow([str(wij), SearchInd[wij]])
            #path2 = 'data/*.txt'
            files2 = glob.glob(path)
            for fpath2 in files2:
                file_name = os.path.basename(fpath2)
                fid = client.file_id(file_name)
                ### Creating Array of File IDs and File Names
                fileid_dict[fid] = file_name
                #print fpath2
                datafiles = file(fpath2)

                for ln in datafiles:
                    #stripln = ln.strip()
                    # Convert the characters in line to lowercase to avoid case mismatch
                    #ln = ln.lower()
                    #print line2
                    if wij in ln:
                        #print wij
                        dfiles[wij] += 1
                        print  dfiles[wij]

                        ''' G (KG,  h(wij)||no. of searches (wij))'''
                        h_wij = client.hash_word(wij)
                        hash_conn_search1 = h_wij + str(SearchInd[wij])
                        K_wij = base64.b64encode(client.G(KG, hash_conn_search1))
                        print "Key of Wij: which is G (KG, h(wij)||no. of searches (wij)) " , K_wij

                        ''' h(K_wij, no. of files (wij) || 0 )'''
                        nfiles_conn_zero = str (str(dfiles[wij]) + str(0))
                        #print h_wd
                        Addr_wij = base64.b64encode(client.H(K_wij,nfiles_conn_zero))
                        print "Address of Wij: Which is h(K_wij, no. of files (wij) || 0 )" , Addr_wij

                        ''' ENC(KSE, id(fi) || no. of files (wij))'''
                        nfiles_conn_fileid = str(fid) + str(dfiles[wij])
                        #print 'No. of files Concatenation with File ID : ', nfiles_conn_fileid
                        Val_wij =  client.ENC(KSE, nfiles_conn_fileid)
                        print "Encrypted Value of Wij: Which is ENC(KSE, id(fi) || no. of files (wij))" , Val_wij
                        Map[Addr_wij] = Val_wij
                        #wmapf.writerow(Addr_wij, Val_wij)
                        wmapf.writerow([Addr_wij,Val_wij])

                        #print "Map:" , count, Map
                        #print "Cout: ", count
                        break
                        #print "key"
                    else:
                        #print "Word is not found"
                        dfiles[wij] = dfiles[wij]
                        #print dfiles[wd]
            wf.writerow([str(wij), dfiles[wij]])

        for fi in files:
            f_name = os.path.splitext(fi)[0]
            CFI = client.File_ENC(KSE, fi)
            with open(f_name + ".enc", "wb") as cf:
                cf.write(CFI)
