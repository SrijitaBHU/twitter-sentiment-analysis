from base_data_source import BaseDataSource
import numpy as np
import random

TRAIN_RATIO = 0.9  # the rest is used as validation set


class DataSource(BaseDataSource):
    def __init__(self, vocab, labeled_data_file, test_data_file,
                 embedding_file, embedding_dim, seq_length):
        self._train = None
        self._validation = None
        self._test = None

        self.vocab = vocab
        self.embedding_dim = embedding_dim
        self.seq_length = seq_length

        # Read labeled data.
        with open(labeled_data_file, "r") as f:
            content = [line.strip().split(" ", 1) for line in f.readlines()]

            labeled_data = (
                np.array([self.vocab.get_tok_ids(s[1], self.seq_length)
                          for s in content]),
                np.array([int(s[0]) for s in content]))

            num_train = int(len(content) * TRAIN_RATIO)
            self._train = (
                labeled_data[0][:num_train],
                labeled_data[1][:num_train])
            for i in np.arange(5):
                print("DA", len(self._train[0][i]))
            self._validation = (
                labeled_data[0][num_train:],
                labeled_data[1][num_train:])
        print("Loaded training set and validation set")

        # Read test data.
        with open(test_data_file, "r") as f:
            content = [line.strip().split(",", 1)[1] for line in f.readlines()]
            self._test = np.array([self.vocab.get_tok_ids(s, self.seq_length)
                                   for s in content])
        print("Loaded test set")

        # Read embeddings.
        embedding_dict = {}
        with open(embedding_file, "r") as f:
            content = [line.strip().split(" ") for line in f.readlines()]
            embedding_dict = dict(
                (l[0], [float(x) for x in l[1:]]) for l in content)
        print("Loaded embeddings")

        # Construct the embedding matrix. Row i has the embedding for the token
        # with tokID i.
        self.embedding_matrix = []
        for i in np.arange(self.vocab.vocab_size):
            token = self.vocab.sorted_vocab[i]

            # TODO: Figure out what to do with "<unk>". Currently not in the
            # pretrained embeddings.

            # TODO: Maybe figure out what to do with tokens that appear in our
            # vocabulary, but don't appear in the word embeddings.
            # XXX: currently we insert a random embedding for words that are not
            # in the embedding matrix, but what we could do is ignore these
            # words when we create the vocabulary.
            if token not in embedding_dict:
                self.embedding_matrix.append([
                    random.random()
                    for i in np.arange(self.embedding_dim)])
            else:
                self.embedding_matrix.append(embedding_dict[token])

        self.embedding_matrix = np.array(self.embedding_matrix)
        print("Contructed embedding matrix")

    def get_embeddings(self):
        return self.embedding_matrix

    def train(self, num_samples=None):
        if num_samples is None:
            num_samples = self._train[0].shape[0]

        return (
            self._train[0][:num_samples],
            self._train[1][:num_samples])

    def validation(self, num_samples=None):
        if num_samples is None:
            num_samples = self._validation[0].shape[0]

        return (
            self._validation[0][:num_samples],
            self._validation[1][:num_samples])

    def test(self, num_samples=None):
        if num_samples is None:
            num_samples = self._test.shape[0]

        return self._test[:num_samples]
