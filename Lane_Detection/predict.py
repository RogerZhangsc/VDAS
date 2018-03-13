#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 12:24:10 2018

@author: roger
Tick tick
"""

import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.framework import dtypes

import os, sys
import numpy as np
import math
from datetime import datetime
import time
from PIL import Image
from math import ceil
from tensorflow.python.ops import gen_nn_ops
# modules
from Utils import _variable_with_weight_decay, _variable_on_cpu, _add_loss_summaries, _activation_summary, print_hist_summery, get_hist, per_class_acc, writeImage
from Inputs import *
from model import *
import cv2

def predict(FLAGS):

  test_ckpt = FLAGS.predict
  image_w = FLAGS.image_w
  image_h = FLAGS.image_h
  image_c = FLAGS.image_c
  # testing should set BATCH_SIZE = 1
  batch_size = 1
  
    
  test_data_node = tf.placeholder(
        tf.float32,
        shape=[batch_size, image_h, image_w, image_c])



  phase_train = tf.placeholder(tf.bool, name='phase_train')

  logits = inference_predict(test_data_node, batch_size, phase_train)

  pred = tf.argmax(logits, axis=3)
  # get moving avg
  variable_averages = tf.train.ExponentialMovingAverage(
                      MOVING_AVERAGE_DECAY)
  variables_to_restore = variable_averages.variables_to_restore()

  saver = tf.train.Saver(variables_to_restore)

  # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.0001)

  with tf.Session() as sess:
    # Load checkpoint
    saver.restore(sess, test_ckpt )



    threads = tf.train.start_queue_runners(sess=sess)
    hist = np.zeros((NUM_CLASSES, NUM_CLASSES))
    i = 0
    cap = cv2.VideoCapture('test2.avi')
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('2classoutputtest2mask.avi',fourcc, 10.0, (480,360))
    print('start generating video')
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret==0:
          break
      frame = frame.reshape(1, 360, 480, 3)
      feed_dict = {test_data_node: frame, phase_train: False}

      dense_prediction, im = sess.run([logits, pred], feed_dict=feed_dict)
      im = colorImage(im[0])
      image = cv2.addWeighted(np.uint8(frame[0]), 1, np.uint8(im), 1, 0)
      out.write(np.uint8(image))
      # output_image to verify
#      if (FLAGS.save_image):
#          writeImage(im[0], 'testing_image.png')

    print('finished generaing video')
    sys.exit(0)
    
def inference_predict(images, batch_size, phase_train):
    # norm1
    norm1 = tf.nn.lrn(images, depth_radius=5, bias=1.0, alpha=0.0001, beta=0.75,
                name='norm1')
    # conv1
    conv1 = conv_layer_with_bn(norm1, [7, 7, images.get_shape().as_list()[3], 64], phase_train, name="conv1")
    # pool1
    pool1, pool1_indices = tf.nn.max_pool_with_argmax(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                           padding='SAME', name='pool1')
    # conv2
    conv2 = conv_layer_with_bn(pool1, [7, 7, 64, 64], phase_train, name="conv2")

    # pool2
    pool2, pool2_indices = tf.nn.max_pool_with_argmax(conv2, ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1], padding='SAME', name='pool2')
    # conv3
    conv3 = conv_layer_with_bn(pool2, [7, 7, 64, 64], phase_train, name="conv3")

    # pool3
    pool3, pool3_indices = tf.nn.max_pool_with_argmax(conv3, ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1], padding='SAME', name='pool3')
    # conv4
    conv4 = conv_layer_with_bn(pool3, [7, 7, 64, 64], phase_train, name="conv4")

    # pool4
    pool4, pool4_indices = tf.nn.max_pool_with_argmax(conv4, ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1], padding='SAME', name='pool4')

    """ End of encoder """
    """ start upsample """
    # upsample4
    # Need to change when using different dataset out_w, out_h
    # upsample4 = upsample_with_pool_indices(pool4, pool4_indices, pool4.get_shape(), out_w=45, out_h=60, scale=2, name='upsample4')
    upsample4 = deconv_layer(pool4, [2, 2, 64, 64], [batch_size, 45, 60, 64], 2, "up4")
    # decode 4
    conv_decode4 = conv_layer_with_bn(upsample4, [7, 7, 64, 64], phase_train, False, name="conv_decode4")

    # upsample 3
    # upsample3 = upsample_with_pool_indices(conv_decode4, pool3_indices, conv_decode4.get_shape(), scale=2, name='upsample3')
    upsample3= deconv_layer(conv_decode4, [2, 2, 64, 64], [batch_size, 90, 120, 64], 2, "up3")
    # decode 3
    conv_decode3 = conv_layer_with_bn(upsample3, [7, 7, 64, 64], phase_train, False, name="conv_decode3")

    # upsample2
    # upsample2 = upsample_with_pool_indices(conv_decode3, pool2_indices, conv_decode3.get_shape(), scale=2, name='upsample2')
    upsample2= deconv_layer(conv_decode3, [2, 2, 64, 64], [batch_size, 180, 240, 64], 2, "up2")
    # decode 2
    conv_decode2 = conv_layer_with_bn(upsample2, [7, 7, 64, 64], phase_train, False, name="conv_decode2")

    # upsample1
    # upsample1 = upsample_with_pool_indices(conv_decode2, pool1_indices, conv_decode2.get_shape(), scale=2, name='upsample1')
    upsample1= deconv_layer(conv_decode2, [2, 2, 64, 64], [batch_size, 360, 480, 64], 2, "up1")
    # decode4
    conv_decode1 = conv_layer_with_bn(upsample1, [7, 7, 64, 64], phase_train, False, name="conv_decode1")
    """ end of Decode """
    """ Start Classify """
    # output predicted class number (6)
    with tf.variable_scope('conv_classifier') as scope:
      kernel = _variable_with_weight_decay('weights',
                                           shape=[1, 1, 64, NUM_CLASSES],
                                           initializer=msra_initializer(1, 64),
                                           wd=0.0005)
      conv = tf.nn.conv2d(conv_decode1, kernel, [1, 1, 1, 1], padding='SAME')
      biases = _variable_on_cpu('biases', [NUM_CLASSES], tf.constant_initializer(0.0))
      conv_classifier = tf.nn.bias_add(conv, biases, name=scope.name)

    logit = conv_classifier


    return logit 

def colorImage(image):
    """ store label data to colored image """
    Sky = [0,0,0]
    Building = [0,0,0]
    Pole = [0,0,0]
    Road_marking = [255,69,0]
    Road = [128,64,128]
    Pavement = [0,0,0]
    Tree = [0,0,0]
    SignSymbol = [0,0,0]
    Fence = [0,0,0]
    Car = [0,0,0]
    Pedestrian = [0,0,0]
    Bicyclist = [0,0,0]
    Unlabelled = [0,0,0]
#    Sky = [128,128,128]
#    Building = [128,0,0]
#    Pole = [192,192,128]
#    Road_marking = [255,69,0]
#    Road = [128,64,128]
#    Pavement = [60,40,222]
#    Tree = [128,128,0]
#    SignSymbol = [192,128,128]
#    Fence = [64,64,128]
#    Car = [64,0,128]
#    Pedestrian = [64,64,0]
#    Bicyclist = [0,128,192]
#    Unlabelled = [0,0,0]
    
    r = image.copy()
    g = image.copy()
    b = image.copy()
    label_colours = np.array([Sky, Building, Pole, Road_marking, Road, Pavement, Tree, SignSymbol, Fence, Car, Pedestrian, Bicyclist, Unlabelled])
    for l in range(0,12):
        r[image==l] = label_colours[l,0]
        g[image==l] = label_colours[l,1]
        b[image==l] = label_colours[l,2]
    rgb = np.zeros((image.shape[0], image.shape[1], 3))
    rgb[:,:,0] = r/1.0
    rgb[:,:,1] = g/1.0
    rgb[:,:,2] = b/1.0
    im = Image.fromarray(np.uint8(rgb))
    im = np.array(im)
    return rgb 