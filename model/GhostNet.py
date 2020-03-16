# -- coding: utf-8 --

import os
from module import GhostBottleneck, reshapes ,softmaxs, squeezes
from keras import Input, Model
from keras.layers import Conv2D, BatchNormalization, Activation, GlobalAveragePooling2D, Dropout, Lambda
from keras.optimizers import Adam
from keras.utils import plot_model
#from keras.activations import softmax

class GhostModel(object):
    def __init__(self,numclass,size,channel):
        self.numclass = numclass
        self.size = size
        self.channel = channel
        self.build_model()

    def build_model(self):
        self.model = self.GhostNet()
 
    def GhostNet(self):
        inputdata = Input(shape=(self.size, self.size, self.channel))
        
        x = Conv2D(16,(3,3),strides=(2,2),padding='same',data_format='channels_last',activation=None,use_bias=False)(inputdata)
        x = BatchNormalization(axis=-1)(x)
        x = Activation('relu')(x)
    
        x = GhostBottleneck(x,3,1,16,16,2,False)
        x = GhostBottleneck(x,3,2,48,24,2,False)
        x = GhostBottleneck(x,3,1,72,24,2,False)
        x = GhostBottleneck(x,5,2,72,40,2,True)
        x = GhostBottleneck(x,5,1,120,40,2,True)
        x = GhostBottleneck(x,3,2,240,80,2,False)
        x = GhostBottleneck(x,3,1,200,80,2,False)
        x = GhostBottleneck(x,3,1,184,80,2,False)
        x = GhostBottleneck(x,3,1,184,80,2,False)
        x = GhostBottleneck(x,3,1,480,112,2,True)
        x = GhostBottleneck(x,3,1,672,112,2,True)
        x = GhostBottleneck(x,5,2,672,160,2,True)
        x = GhostBottleneck(x,5,1,960,160,2,False)
        x = GhostBottleneck(x,5,1,960,160,2,True)
        x = GhostBottleneck(x,5,1,960,160,2,False)
        x = GhostBottleneck(x,5,1,960,160,2,True)
    
        x = Conv2D(960,(1,1),strides=(1,1),padding='same',data_format='channels_last',activation=None,use_bias=False)(x)
        x = BatchNormalization(axis=-1)(x)
        x = Activation('relu')(x)

        x = GlobalAveragePooling2D(data_format='channels_last')(x)
        #x = Reshape((1,1,int(x.shape[1])))(x)
        x = Lambda(reshapes)(x)
        x = Conv2D(1280,(1,1),strides=(1,1),padding='same',data_format='channels_last',activation=None,use_bias=False)(x)
        x = BatchNormalization(axis=-1)(x)
        x = Activation('relu')(x)

        x = Dropout(0.05)(x)
        x = Conv2D(self.numclass,(1,1),strides=(1,1),padding='same',data_format='channels_last',activation=None,use_bias=False)(x)
        #x = K.squeeze(x,1)
        #x = K.squeeze(x,1)
        #out = softmax(x)
        x = Lambda(squeezes)(x)
        x = Lambda(squeezes)(x)
        out = Lambda(softmaxs)(x)
        
        
        model = Model(inputdata, out)
        plot_model(model, to_file=os.path.join('weight', "GhostNet_model.png"), show_shapes=True)
        model.compile(loss='categorical_crossentropy', optimizer=Adam(),metrics=['accuracy']) 
        return model                 
