import json
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_images_and_masks(data, image_folder):
    images = data['images']
    annotations = data['annotations']
    image_files = [image['file_name'] for image in images]

    masks = {}
    images_data = []
    
    for img_file in image_files:
        img_id = next(item for item in images if item['file_name'] == img_file)['id']
        
        mask = np.zeros((images[0]['height'], images[0]['width']), dtype=np.uint8)
        image_annotations = [ann for ann in annotations if ann['image_id'] == img_id]
        
        for ann in image_annotations:
            if 'segmentation' in ann and ann['segmentation']:
                try:
                    if isinstance(ann['segmentation'], list): 
                        for seg in ann['segmentation']:
                            poly_points = np.array(seg, dtype=np.int32).reshape(-1, 2)
                            mask = cv2.fillPoly(mask, [poly_points], 255)  
                    else: 
                        print(f"Skipping invalid segmentation for {img_file}")
                except Exception as e:
                    print(f"Error processing segmentation for {img_file}: {e}")
                    continue 
        
        img_path = os.path.join(image_folder, img_file)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (images[0]['width'], images[0]['height'])) 
        
        images_data.append(img) 
        masks[img_file] = mask 

    return image_files, masks, images_data 

def plot_images_and_masks(images, masks, image_files, num_samples=1):
    for i in range(num_samples):
        plt.figure(figsize=(10, 5))
        
        # Görseli
        plt.subplot(1, 2, 1)
        plt.title(f"Image: {image_files[i]}")
        plt.imshow(images[i])
        
        # Maskeyi
        plt.subplot(1, 2, 2)
        plt.title(f"Mask: {image_files[i]}")
        plt.imshow(masks[image_files[i]], cmap='gray')
        
        plt.show()

train_image_folder = 'train'
test_image_folder = 'test'

train_data = load_json('train/_annotations_train.coco_updated.json')
test_data = load_json('test/_annotations_test.coco_updated.json')

train_image_files, train_masks, train_images = get_images_and_masks(train_data, train_image_folder)
test_image_files, test_masks, test_images = get_images_and_masks(test_data, test_image_folder)

sample_train_idx = random.randint(0, len(train_images)-1)
sample_test_idx = random.randint(0, len(test_images)-1)

sample_train_image = train_images[sample_train_idx]
sample_train_mask = train_masks[train_image_files[sample_train_idx]]
sample_train_image_file = train_image_files[sample_train_idx]

sample_test_image = test_images[sample_test_idx]
sample_test_mask = test_masks[test_image_files[sample_test_idx]]
sample_test_image_file = test_image_files[sample_test_idx]

# Görselleri ve maskeleri görselleştirelim
plt.figure(figsize=(10, 5))

# Train örneği
plt.subplot(1, 2, 1)
plt.title(f"Train Image: {sample_train_image_file}")
plt.imshow(sample_train_image)

plt.subplot(1, 2, 2)
plt.title(f"Train Mask: {sample_train_image_file}")
plt.imshow(sample_train_mask, cmap='gray')

plt.show()

# Test örneği
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title(f"Test Image: {sample_test_image_file}")
plt.imshow(sample_test_image)

plt.subplot(1, 2, 2)
plt.title(f"Test Mask: {sample_test_image_file}")
plt.imshow(sample_test_mask, cmap='gray')

plt.show()
