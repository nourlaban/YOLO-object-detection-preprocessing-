import os
import scipy.misc as misc
from xml.dom.minidom import Document
import numpy as np
import copy, cv2

def save_to_xml(save_path, im_height, im_width, objects_axis, label_name):
    object_num = len(objects_axis)
    imgwidth = 800
    imaghight = 800
       
    
    alltext = []
    for i in range(object_num):
        
        x1 = int(objects_axis[i][0])
        y1 = int(objects_axis[i][1])
        x2 = int(objects_axis[i][2])
        y2 = int(objects_axis[i][3])
        x3 = int(objects_axis[i][4])
        y3 = int(objects_axis[i][5])
        x4 = int(objects_axis[i][6])
        y4 = int(objects_axis[i][7])
        clsindx = int(objects_axis[i][8])
        
        xs = [x1,x2,x3,x4]
        ys = [y1,y2,y3,y4]
        
        xmin =   min(xs)
        ymin =   min(ys)
        
        xmax =   max(xs)
        ymax =   max(ys)
        
        width  = xmax - xmin
        height = ymax - ymin
        
        
        xc = xmin +  width   / 2.0
        yc = ymin +  height  / 2.0
        lst = str(clsindx) + " "+  str(xc * 1.0 / imgwidth ) +" " + str(yc * 1.0 / imaghight)  + " " +  str(width * 1.0 / imgwidth) +" " + str(height * 1.0 / imaghight)
        alltext.append(lst + "\n")       
        
    f = open(save_path,'w')
    f.writelines(alltext)
    f.close() 

class_list = ['plane', 'ship' , 'small-vehicle'] 




def format_label(txt_list):
    format_data = []
    for i in txt_list[2:]:
        format_data.append(
        [int(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8])]
        # {'x0': int(i.split(' ')[0]),
        # 'x1': int(i.split(' ')[2]),
        # 'x2': int(i.split(' ')[4]),
        # 'x3': int(i.split(' ')[6]),
        # 'y1': int(i.split(' ')[1]),
        # 'y2': int(i.split(' ')[3]),
        # 'y3': int(i.split(' ')[5]),
        # 'y4': int(i.split(' ')[7]),
        # 'class': class_list.index(i.split(' ')[8]) if i.split(' ')[8] in class_list else 0, 
        # 'difficulty': int(i.split(' ')[9])}
        )
        if i.split(' ')[8] not in class_list :
            print ('warning found a new label :', i.split(' ')[8])
            exit()
    return np.array(format_data)

def clip_image(file_idx, image, boxes_all, width, height):
    if len(boxes_all) > 0:
    # print ('image shape', image.shape)
        shape = image.shape
        for start_h in range(0, shape[0], 512):
            for start_w in range(0, shape[1], 512):
                boxes = copy.deepcopy(boxes_all)
                box = np.zeros_like(boxes_all)
                start_h_new = start_h
                start_w_new = start_w
                if start_h + height > shape[0]:
                  start_h_new = shape[0] - height
                if start_w + width > shape[1]:
                  start_w_new = shape[1] - width
                top_left_row = max(start_h_new, 0)
                top_left_col = max(start_w_new, 0)
                bottom_right_row = min(start_h + height, shape[0])
                bottom_right_col = min(start_w + width, shape[1])


                subImage = image[top_left_row:bottom_right_row, top_left_col: bottom_right_col]
                box[:, 0] = boxes[:, 0] - top_left_col
                box[:, 2] = boxes[:, 2] - top_left_col
                box[:, 4] = boxes[:, 4] - top_left_col
                box[:, 6] = boxes[:, 6] - top_left_col

                box[:, 1] = boxes[:, 1] - top_left_row
                box[:, 3] = boxes[:, 3] - top_left_row
                box[:, 5] = boxes[:, 5] - top_left_row
                box[:, 7] = boxes[:, 7] - top_left_row
                box[:, 8] = boxes[:, 8]
                center_y = 0.25*(box[:, 1] + box[:, 3] + box[:, 5] + box[:, 7])
                center_x = 0.25*(box[:, 0] + box[:, 2] + box[:, 4] + box[:, 6])
                # print('center_y', center_y)
                # print('center_x', center_x)
                # print ('boxes', boxes)
                # print ('boxes_all', boxes_all)
                # print ('top_left_col', top_left_col, 'top_left_row', top_left_row)

                cond1 = np.intersect1d(np.where(center_y[:]>=0 )[0], np.where(center_x[:]>=0 )[0])
                cond2 = np.intersect1d(np.where(center_y[:] <= (bottom_right_row - top_left_row))[0],
                                        np.where(center_x[:] <= (bottom_right_col - top_left_col))[0])
                idx = np.intersect1d(cond1, cond2)
                # idx = np.where(center_y[:]>=0 and center_x[:]>=0 and center_y[:] <= (bottom_right_row - top_left_row) and center_x[:] <= (bottom_right_col - top_left_col))[0]
                # save_path, im_width, im_height, objects_axis, label_name
                if len(idx) > 0:
                    txt = os.path.join(save_dir, 'words', "%s_%04d_%04d.txt" % (file_idx, top_left_row, top_left_col))
                    save_to_xml(txt, subImage.shape[0], subImage.shape[1], box[idx, :], class_list)
                    # print ('save xml : ', xml)
                    if subImage.shape[0] > 5 and subImage.shape[1] >5:
                        img = os.path.join(save_dir, 'words', "%s_%04d_%04d.png" % (file_idx, top_left_row, top_left_col))
                        cv2.imwrite(img, subImage)
        
    
    

print ('class_list', len(class_list))
#raw_data = '/home/aasernour/RRPN_Faster-RCNN_Tensorflow/VOCdevkit/VOCdevkit_test/a/'
raw_images_dir =r'E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\cwords\exper7\rawimages\\' 
raw_label_dir = r'E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\apcs_lables\allvallabelTxt\\'

save_dir = r"E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\cwords\exper7\\" 

images = [i for i in os.listdir(raw_images_dir) if 'png' in i]
labels = [i for i in os.listdir(raw_label_dir) if 'txt' in i]

print ('find image', len(images))
print ('find label', len(labels))

min_length = 1e10
max_length = 1


for idx, img in enumerate(images):
    # img = 'P2330.png'
    print (idx, 'read image', img)
    img_data = misc.imread(os.path.join(raw_images_dir, img))
    # img_data = cv2.imread(os.path.join(raw_images_dir, img))
    # if len(img_data.shape) == 2:
        # img_data = img_data[:, :, np.newaxis]
        # print ('find gray image')

    txt_data = open(os.path.join(raw_label_dir, img.replace('png', 'txt')), 'r').readlines()
    # print (idx, len(format_label(txt_data)), img_data.shape)
    # if max(img_data.shape[:2]) > max_length:
        # max_length = max(img_data.shape[:2])
    # if min(img_data.shape[:2]) < min_length:
        # min_length = min(img_data.shape[:2])
    # if idx % 50 ==0:
        # print (idx, len(format_label(txt_data)), img_data.shape)
        # print (idx, 'min_length', min_length, 'max_length', max_length)
    box = format_label(txt_data)
    clip_image(img.strip('.png'), img_data, box, 800, 800)
    
    
    
    


