import sys
sys.path.append('.')
sys.path.append('Models')
from RangeViT import *
from utils import *

import numpy as np
import os
import torch
import torch.nn as nn
import torchvision
import torch.nn.functional as F
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
import torch.utils.data as data
import torchvision.transforms as transforms
from matplotlib import pyplot as plt
from PIL import Image


PATH_TO_MODEL = sys.argv[1]


#!pip install transformers

from transformers import AutoImageProcessor, SegformerForSemanticSegmentation
model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b0-finetuned-ade-512-512")

import torch.nn as nn
model.segformer.encoder.patch_embeddings[0].proj=nn.Conv2d(5, 32, kernel_size=(7, 7), stride=(4, 4), padding=(3, 3))
model.decode_head.classifier = nn.Conv2d(256, 20, kernel_size=(1, 1), stride=(1, 1))

device = torch.device("cuda")
model.load_state_dict(torch.load(PATH_TO_MODEL))
model.to(device)






val_set = RangeKitti('range_dataset', mode='test')



val_loader = data.DataLoader(
        val_set,
        batch_size=2,
        shuffle=True,
        num_workers=2)

model.cuda()

##

# here are the training parameters
batch_size = 32

criterion = nn.CrossEntropyLoss(weight=weights.cuda().float())
# We are going to use the CrossEntropyLoss loss function as it's most
# frequentely used in classification problems with multiple classes which
# fits the problem. This criterion  combines LogSoftMax and NLLLoss.


# Evaluation metric
ignore_index=[]
#ignore_index0 = list(class_encoding).index('unlabeled')
ignore_index.append(0)
metric = IoU(20, ignore_index=ignore_index)


loss, (iou, miou) = test_for_segformer(model, val_loader, criterion, metric)
print(">>>> [Test] Avg. loss: {0:.4f} | Mean IoU: {1:.4f}".format(loss, miou))


    
    

