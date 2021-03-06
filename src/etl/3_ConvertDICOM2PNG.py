###########
# IMPORTS #
###########
import numpy as np 
import scipy.misc 
import pydicom 
import glob 
import sys
import os, json 

WDIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(WDIR, "../../SETTINGS.json")) as f: 
    SETTINGS_JSON = json.load(f) 

##########
# SCRIPT #
##########

train_dicoms_dir = os.path.join(WDIR, "../../", SETTINGS_JSON["RAW_TRAIN_DICOMS_DIR"])
test_dicoms_dir  = os.path.join(WDIR, "../../", SETTINGS_JSON["RAW_TEST_DICOMS_DIR"])


##########
# DEBUG # 
##########

list_of_train_dicoms = glob.glob(os.path.join(train_dicoms_dir, "*"))
list_of_test_dicoms  = glob.glob(os.path.join(test_dicoms_dir, "*"))
##########


train_images_dir = os.path.join(WDIR, "../../", SETTINGS_JSON["TRAIN_IMAGES_CLEAN_DIR"], "orig")
test_images_dir  = os.path.join(WDIR, "../../", SETTINGS_JSON["TEST_IMAGES_CLEAN_DIR"], "orig")

if not os.path.exists(train_images_dir): os.makedirs(train_images_dir)

if not os.path.exists(test_images_dir):  os.makedirs(test_images_dir) 

    
def dicom_to_png_conversion_train(list_of_train_dicoms):
    
    for i, each_train_dicom in enumerate(list_of_train_dicoms): 
        sys.stdout.write("DICOM to PNG conversion: {}/{} ...\r".format(i+1, len(list_of_train_dicoms)))
        sys.stdout.flush() 
        tmp_dicom_array = pydicom.read_file(each_train_dicom).pixel_array
        assert np.min(tmp_dicom_array) >= 0 & np.max(tmp_dicom_array) <= 255
        scipy.misc.imsave(os.path.join(train_images_dir, each_train_dicom.split("/")[-1].replace("dcm", "png")),
                          tmp_dicom_array)

        
def dicom_to_png_conversion_test(list_of_test_dicoms):
   
    for i, each_test_dicom in enumerate(list_of_test_dicoms): 
        sys.stdout.write("DICOM to PNG conversion: {}/{} ...\r".format(i+1, len(list_of_test_dicoms)))
        sys.stdout.flush() 
        tmp_dicom_array = pydicom.read_file(each_test_dicom).pixel_array
        assert np.min(tmp_dicom_array) >= 0 & np.max(tmp_dicom_array) <= 255
        scipy.misc.imsave(os.path.join(test_images_dir, each_test_dicom.split("/")[-1].replace("dcm", "png")),
                          tmp_dicom_array) 
    
    
from multiprocessing import Pool, cpu_count


######### Parallelized version
### train 

n=round(len(list_of_train_dicoms)/cpu_count())
files_train= [list_of_train_dicoms[i:i + n] for i in range(0, len(list_of_train_dicoms), n)]

with Pool(processes=cpu_count()) as pool:  
    pool.map(dicom_to_png_conversion_train, files_train)

### test 

n=round(len(list_of_test_dicoms)/cpu_count())
files_test= [list_of_test_dicoms[i:i + n] for i in range(0, len(list_of_test_dicoms), n)]

with Pool(processes=cpu_count()) as pool:  
    pool.map(dicom_to_png_conversion_train, files_test)
