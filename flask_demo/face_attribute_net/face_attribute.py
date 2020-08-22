import argparse
import torch
import torch.utils.data
import torch.nn as nn
import numpy as np
import os
import pickle
import torchvision
from torch.autograd import Variable
from torchvision import datasets, models, transforms
# from self_network.celeba import CelebA
from .model_res import *

import torch.optim as optim
import torch.nn.functional as F
from os.path import exists, join, basename, dirname
from os import makedirs, remove
import shutil
from torch.optim import lr_scheduler
import math
import PIL.Image as Image

# import matplotlib.pyplot as plt

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
dict_haircolor = {0: "黑色头发",
                  1: "金色头发",
                  2: "棕色头发",
                  3: "灰色头发"}
dict_haircut = {0: "秃头",
                1: "刘海",
                2: "渐退发际线",
                3: "直发",
                4: "卷发"}
dict_sex = {0: "女",
            1: "男"}
dict_beard = {0: "山羊胡",
              1: "胡子",
              2: "无胡子"}
dict_skin = {0: "非白皙皮肤",
             1: "白皙皮肤"}
dict_eyes = {0: "柳叶眉",
             1: "眼袋",
             2: "浓眉",
             3: "戴眼镜",
             4: "窄眼"}

dict_list = [dict_haircolor, dict_haircut, dict_sex, dict_beard, dict_skin, dict_eyes]


def get_FA_model(weight_path):
    '''
    Init face attribute model.
    :param weight_path: the path of weight file.(*.pth)
    :return: model
    '''
    model = AttrPre()
    model.to(device)

    weight = torch.load(weight_path)
    model.load_state_dict(weight)

    return model


def FA_detect(model, pic_path, threshold=0.6):
    '''

    :param model:
    :param pic_path:
    :param threshold:
    :return: final_result
    '''
    with open(pic_path, 'rb') as f:
        img = Image.open(f)
        img = img.convert('RGB')

    print("input image size: [%d,%d]" % (img.size))
    img = img.resize((200, 267), Image.BILINEAR)
    normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5],
                                     std=[0.5, 0.5, 0.5])
    trans = transforms.Compose([
        transforms.ToTensor(),
        normalize,
    ])

    final_result = ["", "", "", "", "", ""]
    temp_result = []
    model.eval()
    with torch.no_grad():
        # 加一个batch的维度，因为训练时有.
        input = trans(img).unsqueeze(0)

        output = model(input.to(device))
        # print(output)
        output_s = [torch.sigmoid(i) for i in output]
        # print(output_s)

        for j in range(6):
            for i in output_s[j]:
                pred_result = i > threshold
                pred_result = pred_result.int()
                temp_result.append(pred_result)
        print(temp_result)

        db_used_result = temp_result.copy()
        print(db_used_result[0].cpu().numpy())



        need_process = [0, 0, 0, 0, 0, 0]
        for l in range(len(temp_result)):
            if 1 in temp_result[l]:
                continue
            else:
                if l == 2 or l == 4:
                    continue
                need_process[l] = 1

        print(output_s)
        for w in [i for i, x in enumerate(need_process) if x == 1]:
            # print(output_s[w].cpu().numpy()[0])
            pred = np.argmax(output_s[w].cpu().numpy()[0])
            final_result[w] = dict_list[w][pred]

            db_used_result[w].cpu().numpy()[pred] = 1

        for w in [i for i, x in enumerate(need_process) if x == 0]:
            # print(temp_result[w].cpu().numpy())
            pred = np.argmax(temp_result[w].cpu().numpy())
            final_result[w] = dict_list[w][pred]

            db_used_result[w].cpu().numpy()[pred] = 1
            

        for j in [2, 4]:
            if temp_result[j] == 1:
                final_result[j] = dict_list[j][1]
            else:
                final_result[j] = dict_list[j][0]

        print(final_result)
        return final_result
