import xml.etree.ElementTree as ET
import random
import os
import cv2
from matplotlib import pyplot as plt
import albumentations as A
from pascal_voc_writer import Writer
import time
import sys
import os
import importlib.util

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

folders = module_from_file("folders", "UDClib/operation/folders.py")
visuals = module_from_file("visuals", "UDClib/object_detection/augmentation/visuals.py")


def save_transform(path, name, img, bbox, class_name):
    image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.path.join(path, name +'.jpg'), image)
    writer = Writer(os.path.join(path, name + '.jpg'), 640, 480)
    writer.addObject(class_name, bbox[0], bbox[1], bbox[2], bbox[3])
    writer.save(os.path.join(path, name +'.xml')) 

def transform(img_path, xml_path, path, loop, augmentation, format, save=True):
    start_time = time.time()
    transform = A.Compose(augmentation, bbox_params=A.BboxParams(format=format))
    for i in range(loop):
        transformed = transform(image=visuals.read_img(img_path), bboxes=visuals.find_bbox(xml_path))
        transformed_image = transformed['image']
        transformed_bboxes = transformed['bboxes']
        new_bbox = [int(i) for i in transformed_bboxes[0][:4]]
        name = os.path.splitext(os.path.basename(img_path))[0]
        if save==True: 
            print('Saving', os.path.join(path, '' + name + 'a' + str(i) + '.jpg'))
            save_transform(path, name + 'a' + str(i), transformed_image, new_bbox, transformed_bboxes[0][4])
        else : return transformed_image, transformed_bboxes
    print('done creating total', loop, 'image augmentation','"' + name + '.jpg"', 'in', (time.time() - start_time), 'seconds')



def transform_image_from_folder(dataset, aug_per_images, augmentation, format, datasetAugmented='dataset_augmented'):
    classData = os.listdir(dataset)
    folders.make_folder(datasetAugmented)
    filename = []
    for cls in classData : filename.append((os.listdir(dataset + '/' + cls)))
    total_time = time.time()
    for i in range(len(filename)):
        folders.make_folder(os.path.join(datasetAugmented, classData[i]))
        for j in filename[i]:
            if j[-3:].lower()=='jpg':
                file_path = j.replace('.jpg', '')
                img_path = os.path.join(dataset, classData[i], file_path + '.jpg')
                xml_path = os.path.join(dataset, classData[i], file_path + '.xml')
                path = os.path.join(datasetAugmented, classData[i])
                transform(img_path, xml_path, path, aug_per_images, augmentation, format)
    print('augmentation done in', time.strftime("%H:%M:%S", time.gmtime(time.time() - total_time)))