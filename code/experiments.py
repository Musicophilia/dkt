import tflearn
import tensorflow as tf
import numpy as np
import os, time

from tf_utils import *
from utils import *

def load_model(model_id, load_checkpoint=False, is_training=False):
    # should be used for all models
    print ('Loading model...')

    if model_id == 'lstm_predict_binary_sequence':
        net = build_lstm_net_predict_sequence()
    elif model_id == 'lstm_predict_binary':
        net = build_lstm_net()

    tensorboard_dir = '../tensorboard_logs/' + model_id + '/'
    checkpoint_path = '../checkpoints/' + model_id + '/'

    print (tensorboard_dir)
    print (checkpoint_path)

    check_if_path_exists_or_create(tensorboard_dir)
    check_if_path_exists_or_create(checkpoint_path)

    if is_training:
        model = tflearn.DNN(net, tensorboard_verbose=2, tensorboard_dir=tensorboard_dir, \
                            checkpoint_path=checkpoint_path, max_checkpoints=3)
    else:
        model = tflearn.DNN(net)

    if load_checkpoint:
        checkpoint = tf.train.latest_checkpoint(checkpoint_path)  # can be none of no checkpoint exists
        if checkpoint and os.path.isfile(checkpoint):
            model.load(checkpoint)
            print ('Checkpoint loaded.')
        else:
            print ('No checkpoint found. ')

    print ('Model loaded.')
    return model


def train_model(model_id, use_checkpoint=True):

    maxlen = 10 # max sequence length
    x, y = load_data_will_student_solve_next_problem(18, minlen=3, maxlen=maxlen)
    print ("Embedding shape: {}".format(x[0][0].shape))

    x = pad_sequences(x, maxlen=maxlen, value=np.zeros(x[0][0].shape))
    y = to_categorical(y, nb_classes=2)

    print ("Seq lengths of first 5 samples (should be 10): {}".format([len(x[i]) for i in xrange(5)]))

    model = load_model(model_id, load_checkpoint=use_checkpoint, training_mode=True)

    date_time_string = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    run_id = "{}_{}".format(model_id, date_time_string)

    model.fit(x, y, n_epoch=32, validation_set=0.1, show_metric=True, snapshot_step=100, run_id=run_id)
