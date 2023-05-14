import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Concatenate, TimeDistributed, Bidirectional
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

os.environ['CUDA_VISIBLE_DEVICES'] = ''

# Load the job listing data from the CSV file
df = pd.read_csv('job_listings.csv')

# Define the maximum number of words to keep in the vocabulary
max_words = 30000

# Tokenize the text data
tokenizer = Tokenizer(num_words=max_words, lower=True, oov_token='<OOV>')
tokenizer.fit_on_texts(df['text'].values)

# Define the maximum length of the sequences
max_len = 200

# Convert the text data to sequences of integers
sequences = tokenizer.texts_to_sequences(df['text'].values)

# Pad the sequences to the same length
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(padded_sequences, padded_sequences, test_size=0.2, random_state=42)

# Define the input and output sequences
encoder_inputs = Input(shape=(max_len,))
decoder_inputs = Input(shape=(max_len,))

# Define the embedding layer
embedding_dim = 256
embedding_layer = Embedding(max_words, embedding_dim)

# Define the encoder LSTM layer
encoder_lstm = LSTM(embedding_dim, return_sequences=True, return_state=True)

# Define the decoder LSTM layer
decoder_lstm = LSTM(embedding_dim, return_sequences=True, return_state=True)

# Encode the input sequences
encoder_embedding = embedding_layer(encoder_inputs)
_, state_h, state_c = encoder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

# Decode the output sequences
decoder_embedding = embedding_layer(decoder_inputs)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)

# Define the attention layer
attention = tf.keras.layers.Attention()
context_vector = attention([decoder_outputs, encoder_embedding])

# Concatenate the context vector and decoder outputs
decoder_combined_context = Concatenate(axis=-1)([context_vector, decoder_outputs])

# Apply a dense layer to the concatenated output
decoder_dense = TimeDistributed(Dense(max_words, activation='softmax'))
decoder_outputs = decoder_dense(decoder_combined_context)

# Define the model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# Train the model with validation data
model.fit([X_train, X_train], y_train, batch_size=32, epochs=11, validation_data=([X_val, X_val], y_val))

# Generate a new job listing
new_job_title = "Systemutveckling"
new_job_text = "Vi söker en skicklig dataanalytiker till vårt team. Den idealiska kandidaten bör ha erfarenhet av dataanalys, statistik och datavisualisering."

# Convert the new job listing to a sequence of integers
new_sequence = tokenizer.texts_to_sequences([new_job_text])
new_padded_sequence = pad_sequences(new_sequence, maxlen=max_len, padding='post')

# Generate a prediction for the new job listing
prediction = model.predict([new_padded_sequence, new_padded_sequence])

# Convert the prediction back to text
new_text = tokenizer.sequences_to_texts(prediction.argmax(axis=-1))[0]

# Print the new job listing
print("Job Title:", new_job_title)
print("Job Text:", new_text)
