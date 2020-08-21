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
dict_haircolor = {0: "black hair",
                  1: "blond hair",
                  2: "brown hair",
                  3: "gray hair"}
dict_haircut = {0: "bald",
                1: "bangs",
                2: "recending hairline",
                3: "straight hair",
                4: "wavy hair"}
dict_sex = {0: "female",
            1: "male"}
dict_beard = {0: "goatee",
              1: "mustache",
              2: "no_beard"}
dict_skin = {0: "no pale skin",
             1: "pale skin"}
dict_eyes = {0: "arched eyebrows",
             1: "bags under eyes",
             2: "bushy eyebrows",
             3: "eye glasses",
             4: "narrow eyes"}

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

        for w in [i for i, x in enumerate(need_process) if x == 0]:
            # print(temp_result[w].cpu().numpy())
            pred = np.argmax(temp_result[w].cpu().numpy())
            final_result[w] = dict_list[w][pred]

        for j in [2, 4]:
            if temp_result[j] == 1:
                final_result[j] = dict_list[j][1]
            else:
                final_result[j] = dict_list[j][0]

        print(final_result)
        return final_result
