import tensorflow as tf
import numpy as np


def build_and_train():

    valid_size = 8
    x_valid = np.random.choice(valid_size * 10, valid_size, replace=False)
    print('valid: {}'.format(x_valid))


    batch_size = 128
    embedding_size = 128
    n_negative_samples = 64
    skip_window = 2

    vocab_len = 123456


    tf.reset_default_graph()


    inputs = tf.placeholder(dtype=tf.int32, shape=[batch_size])
    outputs = tf.placeholder(dtype=tf.int32, shape=[batch_size,1])
    inputs_valid = tf.constant(x_valid, dtype=tf.int32)


    # define embeddings matrix with vocab_len rows and embedding_size columns
    # each row represents vector representation or embedding of a word
    # in the vocabulary
    embed_dist = tf.random_uniform(
        shape=[vocab_len, embedding_size],
        minval=-1.0,
        maxval=1.0
    )
    embed_matrix = tf.Variable(
        embed_dist,
        name='embed_matrix'
    )

    # define the embedding lookup table
    # provides the embeddings of the word ids in the input tensor
    embed_ltable = tf.nn.embedding_lookup(embed_matrix, inputs)


    # define noise-contrastive estimation (NCE) loss layer
    nce_dist = tf.truncated_normal(
        shape=[vocab_len, embedding_size],
        stddev=1.0 /
        tf.sqrt(embedding_size * 1.0)
    )
    nce_w = tf.Variable(nce_dist)
    nce_b = tf.Variable(tf.zeros(shape=[vocab_len]))

    loss = tf.reduce_mean(
        tf.nn.nce_loss(
            weights=nce_w,
            biases=nce_b,
            inputs=embed_ltable,
            labels=outputs,
            num_sampled=n_negative_samples,
            num_classes=vocab_len
        )
    )

    # Compute the cosine similarity between validation set samples
    # and all embeddings.
    norm = tf.sqrt(
        tf.reduce_sum(
            tf.square(embed_matrix),
            1,
            keep_dims=True
        )
    )
    normalized_embeddings = embed_matrix / norm
    embed_valid = tf.nn.embedding_lookup(
        normalized_embeddings,
        inputs_valid
    )
    similarity = tf.matmul(
        embed_valid,
        normalized_embeddings,
        transpose_b=True
    )


    n_epochs = 10
    learning_rate = 0.9
    n_batches = ptb.n_batches_wv()
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

    with tf.Session() as tfs:
        tf.global_variables_initializer().run()
        for epoch in range(n_epochs):
            epoch_loss = 0
            ptb.reset_index()
            for step in range(n_batches):
                x_batch, y_batch = ptb.next_batch_sg()
                y_batch = nputil.to2d(y_batch, unit_axis=1)
                feed_dict = {inputs: x_batch, outputs: y_batch}
                _, batch_loss = tfs.run([optimizer, loss], feed_dict=feed_dict)
                epoch_loss += batch_loss
            epoch_loss = epoch_loss / n_batches
            print('\nAverage loss after epoch ', epoch, ': ', epoch_loss)

            # print closest words to validation set at end of every epoch
            similarity_scores = tfs.run(similarity)
            top_k = 5
            for i in range(valid_size):
                similar_words = (-similarity_scores[i, :]).argsort()[1:top_k + 1]

                similar_str = 'Similar to {0:}:'.format(ptb.id2word[x_valid[i]])
                for k in range(top_k):
                    similar_str = '{0:} {1:},'.format(similar_str, ptb.id2word[similar_words[k]])
                print(similar_str)

        final_embeddings = tfs.run(normalized_embeddings)
