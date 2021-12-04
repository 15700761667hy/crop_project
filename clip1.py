import shutil

import cv2
import os

from PIL import Image


def solvelabel():
    '''
    将标签内容存在列表里
    :return: data ，list
    '''
    labelistdir = os.listdir(labelpath)
    list = []
    for labelname in labelistdir:  # 10张图片
        labelfilepath = os.path.join(labelpath, labelname)  # IPD 文件路径
        data = []  #
        for line in open(labelfilepath, "r"):  # 设置文件对象,并读取每一行文件
            line = line[:-1]  # 去掉换行符 ,line 是 str 格式 ，一个字符串
            # 把字符串用空格分隔成一个一个的字符， line.split() 是一个列表，['2813.042', '0057.449', '0005', '0005']
            data.append(line.split())  # 将每一行文件加入到data
        list.append(data)
    return   list
def solveimg( imglistdir):
    '''
    裁剪图片
    :return: centerpoint ,txtlist
    '''
    txtlist = []  # 图片文件名列表
    id = 0
    for jpgname in imglistdir:
            # 10张图片
         txtlist.append(jpgname.split('.')[0]) #10张图片的名字
         if jpgname.split('.')[1] == 'png' or jpgname.split('.')[1] == 'jpg':
            filepath = os.path.join(imgpath, jpgname)  # 拼凑图片的路径
            img = Image.open(filepath)#打开图片
            h_ini = img.size[0]  # 原图的高 4096
            w_ini = img.size[1]  # 原图的宽
            x = 0
            y = 0
            ####这里需要均匀裁剪几张，就除以根号下多少，这里我需要裁剪64张-》根号64=8（8*8）####
            w = float(img.size[0] / 8)  # 裁剪后的宽 512
            h = float(img.size[1] / 8)  # 裁剪后的高 512
            count = 0
            cenpoint_list = []  # 中心点坐标列表
            for k in range(8):
                for v in range(8):
                    # 得到该裁剪图片的中心点坐标
                    temp_list = []
                    x_cen = (w_ini / 8) / 2 + (w_ini / 8) * v
                    y_cen = (h_ini / 8) / 2 + (h_ini / 8) * k
                    temp_list.append(x_cen)
                    temp_list.append(y_cen)
                    cenpoint_list.append(temp_list)  # 将坐标添加进列表里
                    crop_region = img.crop((x + k * w, y + v * h, x + w * (k + 1), y + h * (v + 1)))#调用库函数
                    newimgpath = newdir + '\\' + jpgname.split(".")[0] + '-' + str(count+1) + '.png'  # 裁剪后的第i张图片的路径
                    # 保存图片的位置以及图片名称
                    crop_region.save(newimgpath)
                    count+=1
         id+=1
    print(len(txtlist))# 10张图片的名字
    print(txtlist[0])
    print(len(cenpoint_list)) # 64个坐标
    return   cenpoint_list , txtlist

def solve():
        # main 函数
        list = solvelabel()
        cenpoint_list, txtlist = solveimg(imglistdir)  #

        for i in range(len(list)):  # 十张图片的数据,len(list) == 10
            for objinfo in list[i]: # 第 i 张图片的目标, n 个数量的目标
                # 遍历列表list ，取出每一个目标的 x , y  , w , h 坐标
                x, y = objinfo[0], objinfo[1]
                w, h = objinfo[2], objinfo[3]
                # 遍历每一个裁剪窗口，看x ,y  是在哪一个窗口内
                for j in range(len(cenpoint_list)):  # xy  为 [256.0, 256.0]  64个中心坐标点
                    x_center, y_center = cenpoint_list[j][0], cenpoint_list[j][1]  # type(x_center)  float类型 窗口的中心坐标
                    # 开始判断x , y  是不是在中心坐标 x_center, y_cener的为中心的窗口范围内。
                    if (((x_center - 256) <= float(x) <= (x_center + 256)) and (
                            (y_center - 256) <= float(y) <= (y_center + 256))):
                        #如果为true ,那么就保存在以x_center , y_center 为中心的窗口对应的txt文件中
                        print(x,y, "是该窗口的目标")
                        # 更正图片的分辨率
                        x = str(format(float(x) % 512, '.3f'))  # 保留三位小数
                        y = str(format(float(y) % 512, '.3f'))
                        # 然后将x, y 坐标 写进去 txt文件
                        newlabel_txt = newlabeldir + '\\' + txtlist[i] + '-' + str(j+1) + '.txt'
                        print(newlabel_txt)
                        file = open(newlabel_txt, 'a')  # 640张标签的路径
                        file.write(x + ' ' + y + ' ' + w + ' ' + h)
                        file.write('\r')



if __name__ == "__main__":
    # 图像文件原始路径
    path = r"C:\Users\19821\Desktop\clipdata"
    imgpath = os.path.join(path, 'device')
    labelpath = os.path.join(path, 'label')
    imglistdir = os.listdir(imgpath)
    # 新建split文件夹用于保存
    newdir = os.path.join(path, 'split')
    #if (os.path.exists(newdir) == True):
    #     shutil.rmtree(newdir)
    if (os.path.exists(newdir) == False):
        os.mkdir(newdir)
    # 新建croplabel文件夹用于保存
    newlabeldir = os.path.join(path, 'croplabel')
    if (os.path.exists(newlabeldir) == True):
        shutil.rmtree(newlabeldir)
    if (os.path.exists(newlabeldir) == False):
        os.mkdir(newlabeldir)

    #main
    global txtlist
    global cenpoint_list
    solve()










