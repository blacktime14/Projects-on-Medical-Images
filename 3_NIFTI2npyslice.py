# CT: preprocessing 후 slice 떼서 저장하기
# Divide into three different orientation-image
import os
import nibabel as nib
import time
import pandas as pd
from pandas import DataFrame as DF
import numpy as np
import cv2


#savepath = '/home/sihyeon/kumed/converted/prep'



# list 이미지용 sort해서 빼기
# 안에서 preprocessing 다 하고
# 1. normalization regarding whole 3D image
# 2. histogram equalization regarding 2D slice image
# 그리고 slice 떼서 npy로 CT 저장

def slice_save(root,orientation,classlabel):
    print(orientation+': '+classlabel)
    saveroot = os.path.join(root, 'prep', orientation, classlabel)
    totalist = list(sorted(os.listdir(os.path.join(root, 'split', orientation, classlabel))))
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

    imglist = list(sorted(imglist))
    annlist = list(sorted(annlist))
    # sanity check
    for i in range(len(imglist)):
        imgid = imglist[i]
        annid = annlist[i]
        assert imgid.replace(imgid[-7:], '') == annid.replace(annid[-5:], '')

    idlist = []
    labelist = []
    print('start!')
    since = time.time()

    for name in list(sorted(imglist)):

        loadimg = nib.load(os.path.join(root, 'split', orientation, classlabel, name))
        imgdata = loadimg.get_data()

        ## intensity noramlization to 0-255 (regarding entire image)
        imgdata = cv2.normalize(imgdata, None, 0, 255, cv2.NORM_MINMAX)
        #print(name+':'+str(imgdata.shape[2]))

        for z in range(imgdata.shape[2]):
            sliceid = name.replace('.nii.gz','_'+str(z)+'.npy')
            #print(sliceid)
            sliceimg = np.squeeze(imgdata[:,:,z])

            ## histogram equalization (regarding slice image)
            hist, bins = np.histogram(sliceimg.flatten(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf_m = np.ma.masked_equal(cdf, 0)
            # History Equalization 공식
            cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
            # Mask처리를 했던 부분을 다시 0으로 변환
            cdf = np.ma.filled(cdf_m, 0).astype('uint8')
            sliceimg = sliceimg.astype(int)
            sliceimg = cdf[sliceimg]
            ################################################################################
            # End of Equalization###########################################################
            ################################################################################

            sliceimg_rgb = np.repeat(sliceimg[..., np.newaxis], 3, -1)

            idlist.append(sliceid)
            if classlabel == 'invertedPapilloma':
                labelist.append(0)
            elif classlabel == 'nasalPolyp':
                labelist.append(1)
            else:
                labelist.append(2)

            path = os.path.join(saveroot,sliceid)
            np.save(path,sliceimg_rgb)

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

    df = DF({"ID": idlist, "label": labelist})
    labelpath = os.path.join(saveroot,'label_info.xlsx')
    writer = pd.ExcelWriter(labelpath, engine="xlsxwriter")
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

def checking(orientation,classlabel):
    root = '/home/sihyeon/kumed/converted'
    saveroot = os.path.join(root, 'prep', orientation, classlabel)
    idlists = os.listdir(saveroot)

    example = np.load(os.path.join(saveroot, idlists[0]))
    print(example.shape)
    print(orientation+classlabel+':'+str(len(idlists)-1))

#checking('axial','normal')

def main():
    root = '/home/sihyeon/kumed/converted'
    orientation = ['coronal','sagittal']
    classlabel = ['invertedPapilloma','nasalPolyp','normal']
    for a in range(2):
        orr = orientation[a]
        for b in range(3):
            clb = classlabel[b]
            slice_save(root, orr, clb)
            checking(orr,clb)

main()

