# Remove abnormal imgs beforehand (exist as one test img)
# rm img_path and ann_path
# before removal,
# nsd: 870 files /np: 3281 files /ip: 538
import os
import nibabel as nib

'''
root = '/home/sihyeon/kumed/converted/classified'
listlabel = os.listdir(root)

for i in range(len(listlabel)): # len(listlabel)
    label = listlabel[i]
    totalist = list(sorted(os.listdir(os.path.join(root,label))))
    print(len(totalist))
    annlist = []
    imglist = []
    templist = []
    # separate ann/img files in root folder
    for file in totalist:
        if file[-5:] == '.json':
            annlist.append(file)
            templist.append(file.replace(file[-5:], ''))
        else:
            imglist.append(file)
    # remove id with no annotation (total 17 imgs)
    for id in imglist:
        partid = id.replace(id[-7:], '')
        if partid in templist:
            continue
        else:
            imglist.remove(id)
    imglist2 = list(sorted(imglist))
    annlist2 = list(sorted(annlist))

    for j in range(len(imglist2)):
        img_path = os.path.join(root,label,imglist2[j])
        ann_path = os.path.join(root,label,annlist2[j])
        loadimg = nib.load(img_path)
        imgdata = loadimg.get_data()

        if imgdata.shape[2] == 1:
            os.system('rm "'+img_path+'"')
            os.system('rm "'+ann_path+'"')
            print(img_path)
'''

# chk orientation info
from MDprep02 import *

root = '/home/sihyeon/kumed/converted'
dataset = OMUCTDataset(root)
print(len(dataset))
print(dataset[0][0].shape)
print(dataset[0][1])

axial = []
sag = []
coronal = []
for i in range(len(dataset)):
    if dataset[i][1]['orientation'] == 'coronal':
        coronal.append(i)
    elif dataset[i][1]['orientation'] == 'axial':
        axial.append(i)
    else:
        sag.append(i)

print(len(axial))
print(len(sag))
print(len(coronal))

root2 = os.path.join(root,'split')
axislist = list(sorted(os.listdir(root2))) # axial-coronal-sagittal 순서
print(axislist)
for i in range(len(dataset)): # len(dataset)
    img = dataset.imgs[i]
    ann = dataset.anns[i]

    img_path = os.path.join(root,'summed',img)
    ann_path = os.path.join(root,'summed',ann)
    if dataset[i][1]['orientation'] == 'axial':
        mv_path1 = os.path.join(root2,axislist[0])
        os.system('cp -r '+img_path+' '+mv_path1)
        os.system('cp -r ' + ann_path + ' ' + mv_path1)
    elif dataset[i][1]['orientation'] == 'coronal':
        mv_path2 = os.path.join(root2, axislist[1])
        os.system('cp -r ' + img_path + ' ' + mv_path2)
        os.system('cp -r ' + ann_path + ' ' + mv_path2)
    else:
        mv_path3 = os.path.join(root2, axislist[2])
        os.system('cp -r ' + img_path + ' ' + mv_path3)
        os.system('cp -r ' + ann_path + ' ' + mv_path3)

# chk
labelist = ['invertedPapilloma','nasalPolyp','normal','nasalSeptalDev']

root1 = '/home/sihyeon/kumed/converted/classified/'+labelist[3]+'/'
root2 = '/home/sihyeon/kumed/converted/split'
listor = os.listdir(root2)
sublist1 = os.listdir(os.path.join(root2,listor[0],labelist[2]))
sublist2 = os.listdir(os.path.join(root2,listor[1],labelist[2]))
sublist3 = os.listdir(os.path.join(root2,listor[2],labelist[2]))
fullist = os.listdir(root1)
newlist = sublist1+sublist2+sublist3
print(len(sublist1)+len(sublist2)+len(sublist3))
print(len(fullist))

print(set(fullist)-set(newlist))