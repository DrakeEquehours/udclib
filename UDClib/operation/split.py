import shutil
import os 
import time 
import importlib
def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

folders = module_from_file("folders", "UDClib/operation/folders.py")

def split_test(datasetAugmented, output='output'):
    classData = os.listdir(datasetAugmented)
    filename = []
    for cls in classData : filename.append((os.listdir(datasetAugmented + '/' + cls)))
    # print(filename)
    folders.make_folder(output)
    folders.make_folder(os.path.join(output, 'train'))
    folders.make_folder(os.path.join(output, 'test'))
    total_time = time.time()
    for i in range(len(filename)):
        count=0
        for j in filename[i]:
            if j[-3:].lower()=='jpg':
                file_path = j.replace('.jpg', '')
                img_path = os.path.join(datasetAugmented, classData[i], file_path + '.jpg')
                xml_path = os.path.join(datasetAugmented, classData[i], file_path + '.xml')
                if count == 4 : 
                    try:
                        shutil.move(img_path, 'output/test')
                        shutil.move(xml_path, 'output/test')
                        count = 0
                    except:
                        print("file already exist, try locate to different folder or delete the files on directory")
                        break
                else : 
                    try:
                        shutil.move(img_path, 'output/train')
                        shutil.move(xml_path, 'output/train')
                    except:
                        print("file already exist, try locate to different folder or delete the files on directory")
                        break
                count += 1