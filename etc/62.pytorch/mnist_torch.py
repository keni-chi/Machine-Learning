import os
import numpy as np
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision import datasets

x =  [d for d in dir(datasets) if 'MNIST' in d]                                                                


x1 = ['EMNIST', 'FashionMNIST', 'KMNIST', 'MNIST', 'QMNIST']



datadir = './MNIST'

transform = transforms.Compose([transforms.ToTensor()])
trainset = datasets.MNIST(datadir, download=True, transform=transform)
trainloader = DataLoader(trainset, batch_size=256, shuffle=True)

tmp = trainloader.__iter__()
x, y = tmp.next()
x2, y2 = tmp.next()

out = x.detach().numpy()
out = out.reshape(8,32,28,28)
out = out.transpose(0,2,1,3)
out = out.reshape(8*28,32*28)
out = (out*255).astype(np.uint8)

