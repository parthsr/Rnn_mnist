import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.ops import rnn,rnn_cell
mnist= input_data.read_data_sets('/home/parth/ml/sentdex',one_hot=True)

hm_epoch= 10
n_classes=10
batch_size=128
n_chunks = 28
chunk_size = 28
rnn_size= 128

x=tf.placeholder('float',[None,n_chunks,chunk_size])
y=tf.placeholder('float')

def recurrent_neural_network (x):

    layer= {'weigths':tf.Variable(tf.random_normal([rnn_size,n_classes])),
            'biases':tf.Variable(tf.random_normal([n_classes]))}

    x = tf.transpose(x, [1,0,2])
    x = tf.reshape(x, [-1, chunk_size])
    x= tf.split(0, n_chunks,x)

    lstm_cell = rnn_cell.BasicLSTMCell(rnn_size)
    outputs,states= rnn.rnn(lstm_cell,x, dtype=tf.float32)
    output= tf.matmul(outputs[-1],layer['weigths']+ layer['biases'])
    return output

def train_neural_network(x):
    prediction = recurrent_neural_network(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y))
    optimiser= tf.train.AdamOptimizer().minimize(cost)

    
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(hm_epoch):
            epoch_loss=0
            for _ in range (int(mnist.train.num_examples/batch_size)):
                epoch_x , epoch_y = mnist.train.next_batch(batch_size)
                epoch_x = epoch_x.reshape(batch_size, n_chunks, chunk_size)
                _, c= sess.run([optimiser,cost],feed_dict={x: epoch_x , y: epoch_y})
                epoch_loss+=c
            print('Epoch ',epoch, 'completed out of ',hm_epoch, 'epoch_loss:', epoch_loss)

        correct=tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
        accuracy= tf.reduce_mean(tf.cast(correct,'float'))
        print('accuracy:', accuracy.eval({x:mnist.test.images.reshape(-1, n_chunks,chunk_size), y:mnist.test.labels}))

train_neural_network(x)
