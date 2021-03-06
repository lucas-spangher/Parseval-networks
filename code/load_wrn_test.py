import sys
import datetime

from models import ResidualBlockProperties, ResNet
from data_utils import Cifar10Loader, Dataset
import standard_resnets
from training import train
import dirs

dimargs = sys.argv[1:]
if len(dimargs) not in [0, 2]:
    print("usage: train-wrn.py [<Zagoruyko-depth> <widening-factor>]")
zaggydepth, k = (16, 4) if len(dimargs) == 0 else map(int, dimargs)

print("Loading and preparing data...")
ds_train, ds_val = Cifar10Loader.load_train_val()
ds_trainval = Dataset.join(ds_train, ds_val)
ds_test = Cifar10Loader.load_test()

print("Initializing model...")
model = standard_resnets.get_wrn(
    zaggydepth, k, ds_train.image_shape, ds_train.class_count)

saved_path = dirs.SAVED_MODELS + '/wrn-28-10-t--2018-01-23-19-13/ResNet'
model.load_state(saved_path)
print(saved_path)
print("Starting training and validation loop...")
train(model, ds_trainval, ds_test, epoch_count=200)