import numpy as np
from keras.preprocessing.sequence import pad_sequences


def pad(sequence, flag, word_per_sent=None, char_per_word=None):
    if flag == 'word' or flag == 'label':
        return pad_sequences(sequence, maxlen=word_per_sent, padding='post', truncating='post')
    elif flag == 'char':
        for i in range(len(sequence)):
            sequence[i] = pad_sequences(sequence[i], maxlen=char_per_word, padding='post', truncating='post')
            if len(sequence[i]) <= word_per_sent:
                pad_width = ((0, word_per_sent - len(sequence[i])), (0, 0))
                sequence[i] = np.pad(sequence[i], pad_width=pad_width, mode='constant', constant_values=0)
            else:
                sequence[i] = sequence[i][:word_per_sent]
        return np.asarray(sequence)
