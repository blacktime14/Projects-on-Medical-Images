# preprocess 01: CT
# CT: DICOM to NIFTI via dcm2niix
import os
import time
import subprocess
from subprocess import call

txtfile = '/home/sihyeon/kumed/run2.txt'
f = open(txtfile, 'w')
root1 = '/home/sihyeon/kumed/ENT/invertedPapilloma'
root2 = '/home/sihyeon/kumed/ENT/nasalPolyp'
root3 = '/home/sihyeon/kumed/ENT/nasalSeptalDev'
listroot = [root1,root2,root3]
listfolder = ['invertedPapilloma','nasalPolyp','nasalSeptalDev']
#print(listroot)
for x in range(len(listroot)): # len(listroot)
    rootname = listroot[x]
    list0 = os.listdir(rootname)
    list0.sort()
    #print(rootname)
    rootres = '/home/sihyeon/kumed/converted/'+listfolder[x]
    os.system('mkdir "'+rootres+'"')

    for i in range(len(list0)-1): # len(list0)-1
        #print(list0[i])
        listid = os.listdir(os.path.join(rootname,list0[i]))
        if 'CT' in listid:
            rootresCT = os.path.join(rootres,list0[i]) + '/'
            #os.system('mkdir "'+rootresCT+'"')

            rootct = os.path.join(rootname,list0[i],'CT')
            listct = os.listdir(rootct)
            for j in range(len(listct)):
                rootDC = os.path.join(rootct,listct[j]) # dir: DICOM files per patient
                #print(rootresCT)
                #print(rootDC)
                dcm2niix = 'dcm2niix -z y -f %i_%t_%s -o "'
                all = dcm2niix+rootres+'" "'+rootDC+'"\n'
                print(all)
                f.write(all)

                #os.system(all)
f.close()

# for code in runlist:
#     subprocess.run(code,shell=True,check=True)