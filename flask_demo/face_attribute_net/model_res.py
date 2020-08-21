from __future__ import print_function, division
import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision.models as models
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.model_zoo as model_zoo


model_urls = {
    'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
    'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
    'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
    'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
    'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
}


class FeatureExtraction(torch.nn.Module):
    def __init__(self):
        super(FeatureExtraction, self).__init__()
        self.resnet = models.resnet18(pretrained=True)
        #self.resnet = models.resnet34(pretrained=False)
        self.resnet = nn.Sequential(*list(self.resnet.children())[:-1])
        # freeze parameters
        #for param in self.vgg.parameters():
        #    param.requires_grad = False
        # move to GPU
        self.resnet.cuda()

    def forward(self, image_batch):
        return self.resnet(image_batch)

class Classifier(nn.Module):
    def __init__(self, output_dim=1):
        super(Classifier, self).__init__()
        self.fc1 = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(128, 4),
        )
        self.fc1.cuda()
        self.fc2 = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(128, 5),
        )
        self.fc2.cuda()
        self.fc3 = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(128, 1),
        )
        self.fc3.cuda()
        self.fc4 = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(128, 3),
        )
        self.fc4.cuda()
        self.fc5 = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(128, 1),
        )
        self.fc5.cuda()
        self.fc6 = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(128, 5),
        )
        self.fc6.cuda()

    def forward(self, x):
        x = x.view(x.size(0), -1) # flatten
        #print(x)
        hair_color = self.fc1(x)
        hair_cut = self.fc2(x)
        sex = self.fc3(x)
        beard = self.fc4(x)
        skin = self.fc5(x)
        eyes = self.fc6(x)
        return hair_color,hair_cut,sex,beard,skin,eyes

class AttrPre(nn.Module):
    def __init__(self):
        super(AttrPre, self).__init__()
        self.FeatureExtraction = FeatureExtraction()
        # 预训练权重
        init_pretrained_weights(self.FeatureExtraction, model_urls['resnet18'])
        output_dim = 1
        self.classifier = Classifier(output_dim)

    def forward(self, img):
        # do feature extraction
        feature = self.FeatureExtraction(img)
        hair_color,hair_cut,sex,beard,skin,eyes = self.classifier(feature)
        return hair_color,hair_cut,sex,beard,skin,eyes

def init_pretrained_weights(model, model_url):
    """
    Initialize model with pretrained weights.
    Layers that don't match with pretrained layers in name or size are kept unchanged.
    """
    pretrain_dict = model_zoo.load_url(model_url)
    model_dict = model.state_dict()
    pretrain_dict = {k: v for k, v in pretrain_dict.items() if k in model_dict and model_dict[k].size() == v.size()}
    model_dict.update(pretrain_dict)
    model.load_state_dict(model_dict)
    print("Initialized model with pretrained weights from {}".format(model_url))

