# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:43:47 2024

@author: lgxsv2
"""
import os 
import glob
import pandas as pd

os.chdir("D:\GeomorphologyPaper\Analysis\DataExtraction\StepOneRiverTwin")
from testSuccess import testSuccess


#%%
output = r"D:\GeomorphologyPaper\Validation"
val_folder_ims = r"D:\GeomorphologyPaper\Validation\ValidationImages\*.tif"
prediction_im_folder = r"D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023"
#%%
names = []
f1s = []
#%%
for label_fp in glob.glob(val_folder_ims):
    im_name = os.path.basename(label_fp)
    P3 = os.path.join(prediction_im_folder, im_name)
    
    r = testSuccess(image_fp=P3, time=False, output=False, display_image=False,
                    save_image=False,
                    label_fp=val_folder_ims[:-6])
    

    names.append(im_name[:-4])
    f1s.append(r['f1-score']['macro avg'])
    
df = pd.DataFrame({'id':names,'f1':f1s})
#%%
print(round(df['f1'].median(), 2)) # round to 2 sf
#%%
fn = os.path.join(output, 'results.csv')
df.to_csv(fn)